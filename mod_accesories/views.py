from django.shortcuts import render, redirect
import mercadopago
import json
from django.core.mail import send_mail
from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from django.db.models import Q
from mi_befashion.models import *
from django.core.paginator import Paginator
import random
#---------------------------------------------------------
#----------------------BEFASHION--------------------------
#---------------------------------------------------------
app_web = "mod_accesories"
nro_nuevos = 2
filtro_modulo="Accesorios"

def index(request):
	producto_destacados=Producto.objects.filter(destacado=True,modulo_idmodulo__nombre=filtro_modulo)
	#--
	producto_nuevos = Producto.objects.filter(modulo_idmodulo__nombre=filtro_modulo).order_by('-idproducto')[:10]
	p = Paginator(producto_nuevos, nro_nuevos)
	page1 = p.page(1)
	producto_nuevos = page1.object_list
	#--
	marca = Marca.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	categoria= Categoria.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	alerta=''
	if request.GET:
	 	alerta= request.GET['a']
	cliente = validateautenticate(request)
	dic={'destacados':producto_destacados,'nuevos':producto_nuevos,'categorias':categoria,'marcas':marca,'alerta':alerta,'cliente':cliente}	
	return render(request,app_web+'/Index.html', dic)

def productos(request):
	print(request.GET)
	bol_id_categoria = False
	if request.GET:
		bol_id_categoria = True
		filters = {}
		id_categoria = request.GET.get('Categoria', '')		
		id_marca = request.GET.get('Marca', '')
		id_talla = request.GET.get('Talla', '')		
		nombre_pro = request.GET.get('Nombre','')

		filters["modulo_idmodulo__nombre"]=filtro_modulo
		if id_categoria!="":
			cad_id_categoria= id_categoria.split(',')			
			filters["categoria_idcategoria__in"]=cad_id_categoria
			
		if id_marca!="":
			cad_id_marca= id_marca.split(',')
			filters["marca_idmarca__in"]=cad_id_marca		

		if id_talla!="":
			cad_id_talla= id_talla.split(',')
			filters["tallas__idtalla__in"]=cad_id_talla		

		if nombre_pro!="":
			filters["nombre__icontains"]=nombre_pro		

		print ("id_categoria:"+str(id_categoria))
		print ("id_marca:"+str(id_marca))		
		print ("filters:"+str(filters))		
	
	if bol_id_categoria ==True:
		productos= Producto.objects.filter(**filters).distinct()
	else :
		productos= Producto.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
			
	#--
	categoria= Categoria.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	marca = Marca.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	talla = Talla.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	cliente = validateautenticate(request)
	dic={'productos':productos,'categorias':categoria,'marcas':marca,'tallas':talla,'cliente':cliente}	
	return render(request,app_web+'/Producto.html',dic)

def item(request,producto):
	if request.method == 'GET':
		producto= Producto.objects.get(slug=producto)
		count = Producto.objects.filter(modulo_idmodulo__idmodulo=producto.modulo_idmodulo.idmodulo).count()

		#--
		filters = {}
		a_codigo = []
		filters["modulo_idmodulo__nombre"]=filtro_modulo
		for x in range(8):    		
			id_product=random.randint(1,count)
			a_codigo.append(id_product)
		print(a_codigo)		
		filters["idproducto__in"]=a_codigo	
		productos= Producto.objects.filter(**filters).distinct()
		print(productos)		
		#--
	else:
		return redirect('/')
	categoria= Categoria.objects.filter(modulo_idmodulo__nombre=filtro_modulo)	
	marca = Marca.objects.filter(modulo_idmodulo__nombre=filtro_modulo)	
	cliente = validateautenticate(request)
	dic={'producto':producto,'categorias':categoria,'marcas':marca,'producto_recomendado':productos,'cliente':cliente}
	return render(request,app_web+'/Item.html',dic)

def contacto(request):
	print("LLEGO AQUIIII 1111111")
	if request.POST:
		email = request.POST['email']
		nombre = request.POST['name']
		mensaje = request.POST['message']		
		template = get_template('mod_accesories/email_contacto.html')
		context = {'nombre': nombre, 'email': email, 'mensaje': mensaje}
		contenido = template.render(context)
		email_from = settings.EMAIL_HOST_USER
		recipient_list = [email,]
		asunto='Contacto a través de la Web Befashion [ Accesories ]'
		send_mail( asunto, contenido, email_from, recipient_list,fail_silently = False)
		url = '/?a=Mensaje%20Enviado#extForm17-o'
	return redirect(url) 

def validateautenticate(request):
	if request.user.is_authenticated:
		user=request.user
		cliente=Cliente.objects.get(user=user)
	else:
		cliente=""
	return cliente

def sobre_nosotros(request):
	categoria= Categoria.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	marca = Marca.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	talla = Talla.objects.filter(modulo_idmodulo__nombre=filtro_modulo)
	#--
	cliente = validateautenticate(request)
	dic={'categorias':categoria,'marcas':marca,'tallas':talla,'cliente':cliente}	
	return render(request,'mod_accesories/sobre_nosotros.html',dic)
