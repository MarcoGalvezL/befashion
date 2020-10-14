from django.shortcuts import render, redirect
from numpy import random
import mercadopago
import json

from .models import *
from .forms import Formulario_Crear_Nuevo
from django.core.mail import send_mail
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
import random
import hmac
import hashlib
import requests
from django.views.decorators.csrf import csrf_exempt

#---------------------------------------------------------
#----------------------BEFASHION--------------------------
#---------------------------------------------------------
app_web =  settings.WEBAPP

def index(request):
	producto_destacados=Producto.objects.filter(destacado=True)[:5]
	#--
	marca = Marca.objects.all()
	#--
	categoria= Categoria.objects.all()
	alerta=''
	if request.GET:
		alerta= request.GET['a']
	cliente=validateautenticate(request)
	dic={'destacados':producto_destacados,'categorias':categoria,'alerta':alerta,'cliente':cliente,'marcas':marca}
	return render(request,app_web+'/Index.html',dic)

def add_carrito(request):
	if request.POST:
		producto = Producto.objects.get(idproducto=request.POST['producto'])
		cantidad = request.POST['cantidad']
		talla = request.POST['talla']
		url_actual = "../"+request.POST['url']
		if producto.promocion is True or producto.preventa is True:
			subtotal=int(cantidad)*producto.precio_promocion
		else:
			subtotal=int(cantidad)*producto.precio
				

		if request.session.get('Carrito', False):
			#get carrito
			id_cart=request.session['Carrito']
			carrito=Carrito.objects.get(idcarrito=id_cart)
			
			#COMENTADO POR MARCO
			#subtotal=int(cantidad)*producto.precio
			test=Carritohasproductos.objects.filter(carrito_idcarrito=carrito,producto_idproducto=producto,talla=talla)
			print(test)
			#Crear carrito has producto
			if test:
				print("enter test producto")
				#Actualizar CarritoHasProducto
				test[0].cantidad+=int(cantidad)
				test[0].subtotal+=subtotal
				test[0].save()
				#Actualizar Carrito
				#request.session['cantidad']=request.session['cantidad']+1
				carrito.total=carrito.total+subtotal
				carrito.save()
				url=url_actual+'/item/'+str(producto.slug)
				return redirect(url)
			
			else:
				#Crear carrito has producto
				carrito_has_p=Carritohasproductos(carrito_idcarrito=carrito,cantidad=cantidad,subtotal=subtotal,producto_idproducto=producto,talla=talla)
				carrito_has_p.save()
				request.session['Cantidad']+=1
				carrito.total=carrito.total+subtotal
				carrito.save()

		else:
			#crear carrito
			carrito= Carrito()
			carrito.save()
			id_cart=carrito.idcarrito
			request.session['Carrito']=id_cart
			#COMENTADO POR MARCO
			#subtotal=int(cantidad)*producto.precio
			#crear carrito has producto
			carrito_has_p=Carritohasproductos(carrito_idcarrito=carrito,cantidad=cantidad,subtotal=subtotal,producto_idproducto=producto,talla=talla)
			carrito_has_p.save()
			#Actualizar carrito
			request.session['Cantidad']=1
			carrito.total=subtotal
			carrito.save()

		url=url_actual+'/item/'+str(producto.slug)
		return redirect(url)

def carrito(request):
	categoria= Categoria.objects.all()	
	cliente=validateautenticate(request)
	dic={'categorias':categoria,'cliente':cliente}
	if 'Carrito' in request.session:
		#print("paso")
		productos_en_carrito=Carritohasproductos.objects.filter(carrito_idcarrito=request.session['Carrito'])
		dic['productos_en_carrito']=productos_en_carrito
		dic['carrito']=Carrito.objects.get(idcarrito=request.session['Carrito'])
	return render(request,app_web+'/Carrito.html',dic)

def del_carrito(request):
	eliminar=Carritohasproductos.objects.filter(idcarritohasproductos=int(request.POST['eliminar']))
	if eliminar:
		eliminar=Carritohasproductos.objects.get(idcarritohasproductos=int(request.POST['eliminar']))
		subtotal=eliminar.subtotal
		carrito=Carrito.objects.get(idcarrito=eliminar.carrito_idcarrito.idcarrito)
		carrito.total=carrito.total-subtotal
		request.session['Cantidad']-=1
		carrito.save()
		eliminar.delete()
		url='../../carrito'
	return redirect(url)

def realizar_pedido(request):	
	if 'Cantidad' not in request.session or request.session['Cantidad'] == 0:
		return redirect('../../carrito')
	else:
		print("No existe Cantidad en Session")
		categoria= Categoria.objects.all()		
		form=Formulario_Crear_Nuevo()
		cliente=validateautenticate(request)
		delivery=Delivery.objects.all()
		dic={'form':form,'categorias':categoria,'cliente':cliente,'delivery':delivery}
		return render(request,app_web+'/Realizar_pedido.html',dic)

def realizar_pedido2(request):
	cliente=validateautenticate(request)
	if request.POST:
		rut=''
		razonsocial=''
		industria=''
		nombre=request.POST['nombre']
		email=request.POST['email']
		telefono=request.POST['telefono']
		direccion=request.POST['direccion']
		tipoDocumento=request.POST['tipoDocumento']

		if tipoDocumento == "factura":
			rut=request.POST['rut']
			razonsocial=request.POST['razonsocial']
			industria=request.POST['industria']

		if 'notas' in request.POST:
			notas=request.POST['notas']
		else: 
			notas=''

		delivery_id=request.POST['delivery']
		delivery=Delivery.objects.get(iddelivery=delivery_id)
		precio_delivery=delivery.precio
		delivery_nombre=delivery.nombre

		id_cart=request.session['Carrito']
		carrito=Carrito.objects.get(idcarrito=id_cart)
		total_delivery=precio_delivery+carrito.total
		productos_en_carrito=Carritohasproductos.objects.filter(carrito_idcarrito=carrito)
		Texto="Productos "+" (carrito id="+str(carrito.idcarrito)+")"+": \n"
		for c in productos_en_carrito:
			cantidad= str(c.cantidad)
			subtotal= str(c.subtotal)
			#talla= str(c.talla)
			producto= str(c.producto_idproducto.nombre)
			#linea=producto+': '+' '+talla+' '+cantidad+' -  $ '+subtotal+'\n'
			linea=producto+': '+' '+cantidad+' -  $ '+subtotal+'\n'
			Texto=Texto+linea

		compra=Pedido(
			nombre=nombre
			,email=email
			,telefono=telefono
			,direccion=direccion
			,notas=notas
			,pedido=Texto
			,delivery_iddelivery=delivery
			,total=carrito.total
			,total_delivery=total_delivery
			,rut=rut
			,razonsocial=razonsocial
			,industria=industria
			)
		compra.save()
		
		#Email de delivery
		template = get_template('befashion/email_compra.html')
		context = {'compra': compra}
		contenido = template.render(context)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = ['heinrrichfacho@gemail.com']
		asunto='Pedido a través de Mi Tienda Online'
		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)
		
		template = get_template('befashion/email_cliente.html')
		context = { 'compra': compra}
		contenido = template.render(context)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email,]
		asunto='Pedido a través de Tienda Online'
		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)

		ObjPago={'preferenceResult':'','preference':''}
		flow_response=''
		Intpago = IntegracionPago.objects.get(idintegrapago=1)
		# INTEGRACIÓN METODO DE PAGO

		if Intpago.metodo_pago==1:
			ObjPago = MercadoPago(Intpago.mp_public_key,Intpago.mp_access_token,compra.idpedido,compra.total_delivery)
		else:
			ojbfw = {
				'fw_url':Intpago.fw_url,
				'fw_secretkey': Intpago.fw_secretkey,
				'fw_apiKey':Intpago.fw_apiKey,
				'idpedido':compra.idpedido,
				'total_delivery':compra.total_delivery,
				'email':email
				}
			flow_response = Flow(ojbfw)
		# FIN INTEGRACIÓN
		compra.save()
		total=carrito.total
		#---
		categoria= Categoria.objects.all()
		#---
		obj = {'titulo':'MercadoPago1', 'MP':ObjPago['preferenceResult'],'Preference':ObjPago['preference'],'FLOWCL':flow_response,'metodo_pago':Intpago.metodo_pago,
		'nombre':'Cat People','carrito_has_p':productos_en_carrito,'compra':compra,'total':total
		,'categorias':categoria,'cliente':cliente
		}
		#Elimina todo lo referente a la session
		#request.session.flush()	
		#Elimina todo excepto lo que empiezan con _ por ejemplo ()
		for key in list(request.session.keys()):
  			if not key.startswith("_"): # skip keys set by the django system
   				del request.session[key]

		return render(request,'befashion/Realizar_pedido_2.html',obj)

	else:
		for key in list(request.session.keys()):
  			if not key.startswith("_"): # skip keys set by the django system
   				del request.session[key]

		print("HOLA MUNDOOO")
		print(cliente)
		dic = {'cliente':cliente,'total':0}
		return redirect("../../",dic)

def realizar_pedido_factura(request):
	if 'Cantidad' not in request.session or request.session['Cantidad'] == 0:
		return redirect('../../carrito')
	else:
		print("No existe Cantidad en Session")
		categoria= Categoria.objects.all()		
		form=Formulario_Crear_Nuevo()
		cliente=validateautenticate(request)
		delivery=Delivery.objects.all()
		dic={'form':form,'categorias':categoria,'cliente':cliente,'delivery':delivery}
		return render(request,app_web+'/realizar_pedido_factura.html',dic)


def MercadoPago(mp_public_key,mp_access_token,id_pedido,total):
	# INTEGRACIÓN CON MERCADO PAGO
	mp = mercadopago.MP(mp_public_key,mp_access_token)
	Nombre_producto="Compra en: Cat People"
	Total=total
	preference = {
			"items": [
			{	
				"id": 'ID-CAT-'+str(id_pedido),
				"title": Nombre_producto,
				"currency_id": "CLP",
				"description": "Compra a Be Fashion",
				"quantity": 1,
				"unit_price": Total
				}
			],"back_urls": {
			"success": "localhost:8000/compra_exito/",
			"failure": "localhost:8000/compra_fallo/",
			"pending": "localhost:8000/compra_proceso/"
			},
			"external_reference": id_pedido
	}
	preferenceResult = mp.create_preference(preference)
	obj = {'preferenceResult':preferenceResult,'preference':preference}
	return obj

def Flow(ojbfw):
	# INTEGRACIÓN CON MERCADO PAGO
	print("ENTRADA DE FLOWWW")
	print(ojbfw['fw_url'])
	secret_key = b""+ojbfw['fw_secretkey'].encode("utf-8")
	image_metadata = {'amount': ojbfw['total_delivery']
		, 'apiKey': ojbfw['fw_apiKey']
		, 'commerceOrder' : 'ID_BF-' + str(ojbfw['idpedido'])
		, 'email' : ojbfw['email']
		, 'subject' : 'PAGO'
		, 'urlConfirmation' : 'http://localhost:8000/compra_fallo/'
		, 'urlReturn' : 'http://localhost:8000/compra_exito/'
		#, 's': signature
		}
	cadenastring = ""
	for attr, value in image_metadata.items():
		print(attr, value)
		cadenastring+= str(attr)+str(value)
	print(cadenastring)
	#cadenastring = "amount"+ str(ojbfw['total_delivery']) +"apiKey725B185F-B22A-4A7C-A898-672EC2L31B1EcommerceOrderID_BF-"+ str(ojbfw['idpedido'])+"email"+ ojbfw['email'] +"subjectPAGOurlConfirmationhttp://localhost:8000/compra_exito/urlReturnhttp://localhost:8000/compra_fallo/"
	#total_params = b"amount1000apiKey725B185F-B22A-4A7C-A898-672EC2L31B1EcommerceOrder"+ str(total) +"email"+ email +"subjectPAGOurlConfirmationhttp://localhost:5000/loginurlReturnhttp://localhost:5000/login"
	total_params= b""+cadenastring.encode("utf-8")
	signature = hmac.new(secret_key, total_params, hashlib.sha256).hexdigest()
	image_metadata['s'] = signature
	print("signature = {0}".format(signature))
	#print("signature = {0}".format("44e13d46dbd31b013f5c1fe2d333e69f73b00f186878fe365a559caf0519020c"))

	url = ojbfw['fw_url']+'payment/create'
	#headers = {'Authorization': 'my-api-key'}

	data = json.dumps(image_metadata)
	#files = {'file': (FILE, open(PATH, 'rb'), 'image/jpg', {'Expires': '0'})}
	r = requests.post(url, data=image_metadata)
	print(r)
	flow_response_obj = json.loads(r.text)
	for i in flow_response_obj:
		print("key: ", i, "val: ", flow_response_obj[i])
	url_flow = flow_response_obj['url']+"?token="+flow_response_obj['token']
	return url_flow

@csrf_exempt
def compra_exito(request):
	if request.GET:
		if 'external_reference' in request.GET:
			preference=request.GET['external_reference']
			exist= Pedido.objects.filter(idpedido=preference).exists()
			if exist:
				compra=Pedido.objects.get(idpedido=preference)
				compra.estado="Pagado"
				compra.save()

	return render(request,'befashion/compra_exito.html')

@csrf_exempt
def compra_fallo(request):
	cliente=validateautenticate(request)
	if request.GET:
		if 'external_reference' in request.GET:
			preference=request.GET['external_reference']
			exist= Pedido.objects.filter(idpedido=preference).exists()
			if exist:
				compra=Pedido.objects.get(idpedido=preference)
				compra.estado="Fallo en Pago"
				compra.save()
	dic={'cliente':cliente}
	return render(request,'befashion/compra_fallo.html',dic)

@csrf_exempt
def compra_proceso(request):
	if request.GET:
		if 'external_reference' in request.GET:
			preference=request.GET['external_reference']
			exist= Pedido.objects.filter(idpedido=preference).exists()
			if exist:
				compra=Compra.objects.get(idpedido=preference)
				compra.estado="Pago en Proceso"
				compra.save()
	return render(request,'befashion/compra_proceso.html')

def validateautenticate(request):
	if request.user.is_authenticated:
		user=request.user
		cliente=Cliente.objects.get(user=user)
	else:
		cliente=""
	return cliente

#---------------------------------------------------------
#-----------------BEFASHION LOGIN-------------------------
#---------------------------------------------------------

def login_view(request):
	if request.POST:
		username = request.POST.get('email')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		if user is not None:
			cliente=Cliente.objects.get(user=user)
			login(request, user)
			dic={'cliente':cliente, 'texto_grande': "Bienvenido",'texto_chico':'Revisa los detalles de tu cuenta a continuación'}
			#print('hola')
			if 'id_cart' in request.session:
				#print("paso")
				productos_en_carrito=CarritoHasProducto.objects.filter(carrito_idcarrito=request.session['id_cart'])
				dic['productos_en_carrito']=productos_en_carrito
				dic['carrito']=Carrito.objects.get(idcarrito=request.session['id_cart'])

			#print(request.session.get('id_cart'))

			return render(request,'befashion/login.html',dic)
		else:
			dic={'texto_grande': "Ingreso para clientes",'texto_chico':'Bienvenido a Botica Providencia Online, ingresa con tu email y contraseña','alerta':"El usuario o la constraseña no coinciden"}
			return render(request,'befashion/login.html',dic)
	else:
		if request.user.is_authenticated:
			user=request.user
			cliente=Cliente.objects.get(user=user)
			dic={'cliente':cliente, 'texto_grande': "Bienvenida Socia",'texto_chico':'Revisa los detalles de tu cuenta a continuación'}
			if 'id_cart' in request.session:
				productos_en_carrito=CarritoHasProducto.objects.filter(carrito_idcarrito=request.session['id_cart'])
				dic['productos_en_carrito']=productos_en_carrito
				dic['carrito']=Carrito.objects.get(idcarrito=request.session['id_cart'])

			#print(request.session.get('id_cart'))
		else:
			dic={'texto_grande': "Ingreso para Socias ADP",'texto_chico':'Bienvenida al portal de socias, ingresa con tus credenciales'}
		
		return render(request, 'befashion/login.html',dic)

def logoutView(request):
	logout(request)
	print("ENTROOO AQUIIIIIIIII ")
	return redirect('/login')

def add_user(request):
	if request.user.is_authenticated:
		user=request.user
		cliente=Cliente.objects.get(user=user)
		titulo="Actualiza tu cuenta en Bifashion"
		Btnsave="Guardar Cambios"
	else:
		cliente=""
		titulo="Crea tu cuenta en Bifashion"
		Btnsave="Crear cuenta"
	dic={'cliente':cliente,'titulo':titulo,'Btnsave':Btnsave}
	return render(request,'befashion/add_user.html',dic)

def user_added(request):
	nombre=request.POST['nombre']
	apellido=request.POST['apellido']
	telefono=request.POST['phone']
	direccion=request.POST['direccion']
	pkcliente=request.POST['pkcliente']
	cliente=validateautenticate(request)

	if pkcliente == "0":
		contrasena=request.POST['password']
		email=request.POST['email']
		exist= User.objects.filter(username=email).exists()
		if exist:
			dic={'titulo':'Usuario ya existe','alerta':'Ya existe una cuenta asociada a este email. Puede recuperar su contraseña en la seccion de Ingreso.'}
			return render(request,'befashion/user_added.html',dic)
		else:
			usuario=User.objects.create_user(username=email,password=contrasena,email=email)
			usuario.save()
			cliente=Cliente(user=usuario,email=email,nombre=nombre,apellido=apellido,contrasena=contrasena,telefono=telefono,direccion=direccion)
			cliente.save()
			dic={'titulo':'Usuario añadido con exito','alerta':'Se añadio correctamente la cuenta, Puede acceder al sistema en la sección de Ingreso.','cliente':cliente}
			return render(request,'befashion/user_added.html',dic)
	else:
		Cliente.objects.filter(pk=pkcliente).update(
            nombre=nombre,
			apellido=apellido,
			telefono=telefono,
			direccion=direccion
        )
		dic={'titulo':'Usuario Modificado con exito','alerta':'Se Actualizo correctamente la cuenta.','cliente':cliente}
	return render(request,'befashion/user_added.html',dic)

def forgot(request):
	return render(request,'befashion/forgot.html')

def forgot2(request):
	new_pass=random.randint(10000,99999)
	email=request.POST['email']
	exist= User.objects.filter(username=email).exists()
	if exist:
		u=User.objects.get(username=email)
		u.set_password(new_pass)
		u.save()
		cliente=Cliente.objects.get(user=u)
		template = get_template('befashion/email_forgot.html')
		context = {'cliente': cliente, 'new_pass': str(new_pass)}
		contenido = template.render(context)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email,]
		asunto='Contraseña olvidadad Befashion'
		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)
		return redirect('../login')
	else:
		return render(request,'befashion/forgot2.html')

def change_pass(request):
	if request.POST:
		user=request.user
		new_pass=request.POST['password']
		user.set_password(new_pass)
		user.save()
		return redirect('../login')
	else:
		cliente=validateautenticate(request)
		dic={'cliente':cliente}
		return render(request,'befashion/change_pass.html',dic)

#---------------------------------------------------------
#----------------------ZONA OUTLET------------------------
#---------------------------------------------------------
# def productos(request):
# 	print(request.GET)
# 	categoria = False
# 	if request.GET:
# 		categoria = True
# 		idpro=request.GET['id']	
# 	if categoria ==True:
# 		productos= Producto.objects.filter(categoria_idcategoria =idpro )
# 	else :
# 		productos= Producto.objects.all()		
# 	
# 	categoria= Categoria.objects.all()
# 	dic={'productos':productos,'categorias':categoria}
# 	return render(request,'mi_cat/productos.html',dic)
# 	return render(request,'befashion/Productos.html',dic)

# def sobre_nosotros(request):
# 	categoria= Categoria.objects.all()
# 	dic={'categorias':categoria}
# 	return render(request,'befashion/Nosotros.html',dic)

# def item(request):
# 	if request.GET:
# 		idpro=request.GET['id']
# 		producto= Producto.objects.get(idproducto=idpro)
# 	else:
# 		return redirect('/')
# 	categoria= Categoria.objects.all()	
# 	dic={'producto':producto,'categorias':categoria}
# 	return render(request,'befashion/Item.html',dic)

# def del_carrito(request):
# 	eliminar=Carritohasproductos.objects.filter(idcarritohasproductos=int(request.POST['eliminar']))
# 	if eliminar:
# 		eliminar=Carritohasproductos.objects.get(idcarritohasproductos=int(request.POST['eliminar']))
# 		subtotal=eliminar.subtotal
# 		carrito=Carrito.objects.get(idcarrito=eliminar.carrito_idcarrito.idcarrito)
# 		carrito.total=carrito.total-subtotal
# 		request.session['Cantidad']-=1
# 		carrito.save()
# 		eliminar.delete()
# 		url='../../carrito'
# 	return redirect(url)

# def realizar_pedido(request):
# 		categoria= Categoria.objects.all()		
# 		form=Formulario_Crear_Nuevo()
# 		dic={'form':form,'categorias':categoria}
# 		return render(request,'befashion/Realizar_pedido.html',dic)


# def realizar_pedido2(request):
# 	if request.POST:
# 		nombre=request.POST['nombre']
# 		email=request.POST['email']
# 		telefono=request.POST['telefono']
# 		direccion=request.POST['direccion']
# 		if 'notas' in request.POST:
# 			notas=request.POST['notas']
# 		else: 
# 			notas=''
# 		delivery_id=request.POST['delivery']
# 		delivery=Delivery.objects.get(iddelivery=delivery_id)
# 		precio_delivery=delivery.precio
# 		delivery_nombre=delivery.nombre

# 		id_cart=request.session['Carrito']
# 		carrito=Carrito.objects.get(idcarrito=id_cart)
# 		total_delivery=precio_delivery+carrito.total
# 		productos_en_carrito=Carritohasproductos.objects.filter(carrito_idcarrito=carrito)
# 		Texto="Productos "+" (carrito id="+str(carrito.idcarrito)+")"+": \n"
# 		for c in productos_en_carrito:
# 			cantidad= str(c.cantidad)
# 			subtotal= str(c.subtotal)
# 			talla= str(c.talla)
# 			producto= str(c.producto_idproducto.nombre)
# 			linea=producto+': '+' '+talla+' '+cantidad+' -  $ '+subtotal+'\n'
# 			linea=producto+': '+' '+cantidad+' -  $ '+subtotal+'\n'
# 			Texto=Texto+linea

# 		compra=Pedido(nombre=nombre,email=email,telefono=telefono,
# 			direccion=direccion,notas=notas,pedido=Texto,
# 			delivery_iddelivery=delivery,total=carrito.total,total_delivery=total_delivery)
# 		compra.save()
		

# 		Email de delivery
# 		template = get_template('befashion/email_compra.html')
# 		context = {'compra': compra}
# 		contenido = template.render(context)
# 		email_from = settings.EMAIL_HOST_USER
# 		recipient_list = ['heinrrichfacho@gemail.com']
# 		asunto='Pedido a través de Mi Tienda Online'
# 		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)
		

# 		template = get_template('befashion/email_cliente.html')
# 		context = { 'compra': compra}
# 		contenido = template.render(context)
# 		email_from = settings.EMAIL_HOST_USER
# 		recipient_list = [email,]
# 		asunto='Pedido a través de Tienda Online'
# 		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)

# 		mp = mercadopago.MP('2545425583027464','Yp3gjXaD5YRwG6V7rLXRLSBA7jYIxV9l')
# 		Nombre_producto="Compra en: Cat People"
# 		Total=compra.total_delivery
# 		preference = {
# 				"items": [
# 				{	
# 					"id": 'ID-CAT-'+str(compra.idpedido),
# 					"title": Nombre_producto,
# 					"currency_id": "CLP",
# 					"description": "Compra a Cat People",
# 					"quantity": 1,
# 					"unit_price": Total
# 					}
# 				],"back_urls": {
# 				"success": "localhost:8000/compra_exito/",
# 				"failure": "localhost:8000/compra_fallo/",
# 				"pending": "localhost:8000/compra_proceso/"
# 				},
# 				"external_reference": compra.idpedido

# 		}
# 		preferenceResult = mp.create_preference(preference)
# 		print(preferenceResult)
# 		print(preferenceResult["response"]["id"])
# 		compra.save()
# 		total=carrito.total
# 		---
# 		categoria= Categoria.objects.all()
# 		---
# 		obj = {'titulo':'MercadoPago1', 'MP':preferenceResult, 'Preference':preference,
# 		'nombre':'Cat People','carrito_has_p':productos_en_carrito,'compra':compra,'total':total
# 		,'categorias':categoria
# 		}
# 		request.session.flush()		
# 		return render(request,'befashion/Realizar_pedido_2.html',obj)

# 	else:
# 		return redirect("../../")

# def contacto(request):
# 	if request.POST:
# 		tel = request.POST['phone']
# 		email = request.POST['email']
# 		nombre = request.POST['name']
# 		mensaje = request.POST['message']
# 		subject = request.POST['subject']		
# 		template = get_template('befashion/email_contacto.html')
# 		context = {'nombre': nombre, 'telefono': tel, 'email': email,'asunto':subject, 'mensaje': mensaje}
# 		contenido = template.render(context)
# 		email_from = settings.EMAIL_HOST_USER
# 		recipient_list = ['heinrrichfacho@gmail.com',]
# 		asunto='Contacto a través de la Web Zona Outlet'
# 		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)
# 		url = '/?a=Mensaje%20Enviado#extForm17-o'
# 	return redirect(url) 



# def compra_exito(request):
# 	if request.GET:
# 		if 'external_reference' in request.GET:
# 			preference=request.GET['external_reference']
# 			exist= Pedido.objects.filter(idpedido=preference).exists()
# 			if exist:
# 				compra=Pedido.objects.get(idpedido=preference)
# 				compra.estado="Pagado"
# 				compra.save()

# 	return render(request,'befashion/compra_exito.html')

# def compra_fallo(request):
# 	if request.GET:
# 		if 'external_reference' in request.GET:
# 			preference=request.GET['external_reference']
# 			exist= Pedido.objects.filter(idpedido=preference).exists()
# 			if exist:
# 				compra=Pedido.objects.get(idpedido=preference)
# 				compra.estado="Fallo en Pago"
# 				compra.save()
# 	return render(request,'befashion/compra_fallo.html')

# def compra_proceso(request):
# 	if request.GET:
# 		if 'external_reference' in request.GET:
# 			preference=request.GET['external_reference']
# 			exist= Pedido.objects.filter(idpedido=preference).exists()
# 			if exist:
# 				compra=Compra.objects.get(idpedido=preference)
# 				compra.estado="Pago en Proceso"
# 				compra.save()
# 	return render(request,'befashion/compra_proceso.html')


