
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.validators import FileExtensionValidator
from django.utils.html import mark_safe
from smart_selects.db_fields import ChainedForeignKey,ChainedManyToManyField
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
#---------------------------------------------------------
#----------------------BEFASHION--------------------------
#---------------------------------------------------------

class Modulo(models.Model):
    idmodulo = models.AutoField(db_column='idmodulo', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=45)
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Modulo'

    def __str__(self):
        # return "name" from translation
        return self.nombre

class Categoria(models.Model):
    idcategoria = models.AutoField(db_column='idcategoria', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=45)
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')

    class Meta:
        managed = True
        db_table = 'Categoria'

    def __str__(self):
        # return "name" from translation
        return self.nombre

class Marca(models.Model):
    idmarca = models.AutoField(db_column='idmarca', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=45)
    foto = models.ImageField(upload_to='img/productos', db_column='Foto', validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])  # Field name made lowercase.    
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')

    class Meta:
        managed = True
        db_table = 'Marca'

    def __str__(self):
        # return "name" from translation
        return self.nombre
    def image_tag(self):
            return mark_safe('<img src="%s" width="150" height="100" />' % (self.foto.url))


class Talla(models.Model):
    idtalla = models.AutoField(db_column='idtalla', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=45)      
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')  # Field name made lowercase.     
    class Meta:
        managed = True
        db_table = 'Talla'

    def __str__(self):
        # return "name" from translation
        return self.nombre

class Promocion(models.Model):
    idpromocion = models.AutoField(db_column='idPromocion', primary_key=True)
    titulo = models.CharField(db_column='Titulo', max_length=45, blank=True, null=True)
    descripcion = models.CharField(db_column='Descripcion', max_length=90, blank=True, null=True)
    nombre_boton = models.CharField(db_column='Boton_Name', max_length=20, blank=True, null=True)
    link_boton = models.CharField(db_column='Link_Boton', max_length=255, blank=True, null=True)
    foto = models.FileField(upload_to='img/promociones', db_column='Foto', validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')

    class Meta:
        managed = True
        db_table = 'Promocion'


class Producto(models.Model):
    idproducto = models.AutoField(db_column='idProducto', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45)  # Field name made lowercase.
    descripcion = models.TextField(db_column='Descripcion', blank=True, null=True)  # Field name made lowercase.
    short = models.CharField(db_column='Short', max_length=90, blank=True, null=True)  # Field name made lowercase.
    precio = models.IntegerField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.
    precio_promocion = models.IntegerField(db_column='Precio promocion', blank=True, null=True)  # Field name made lowercase.
    destacado = models.BooleanField(db_column='Destacado', default=False)  # Field name made lowercase.
    foto = models.FileField(upload_to='img/productos', db_column='Foto 1', validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])])  # Field name made lowercase.
    foto2 = models.FileField(upload_to='img/productos', db_column='Foto 2', validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])], blank=True, null=True)  # Field name made lowercase.
    foto3 = models.FileField(upload_to='img/productos', db_column='Foto 3', validators=[FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])], blank=True, null=True)  # Field name made lowercase.
    #promocion = models.IntegerField(db_column='Promocion', blank=True, null=True)  # Field name made lowercase.
    promocion = models.BooleanField(db_column='Promocion',default=False)  # Field name made lowercase.
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')  # Field name made lowercase.   
    #categoria_idcategoria = models.ForeignKey(Categoria, models.CASCADE, db_column='categoria_idcategoria')  # Field name made lowercase.  
    activo = models.BooleanField(db_column='Activo',default=True)
    categoria_idcategoria= ChainedForeignKey(
        Categoria,
        chained_field="modulo_idmodulo",
        chained_model_field="modulo_idmodulo",
      )
    #marca_idmarca = models.ForeignKey(Marca, models.CASCADE, db_column='marca_idmarca')  # Field name made lowercase.   
    marca_idmarca= ChainedForeignKey(
        Marca,
        chained_field="modulo_idmodulo",
        chained_model_field="modulo_idmodulo",
      )
    # genero = models.CharField(db_column='Genero', max_length=45, blank=True, null=True)  # Field name made lowercase.
    #preventa = models.IntegerField(db_column='Pre venta', blank=True, null=True)  # Field name made lowercase.
    preventa = models.BooleanField(db_column='Pre venta',default=False)  # Field name made lowercase.
    #talla_idtalla = models.ForeignKey(Talla, models.CASCADE, db_column='talla_idtalla')  # Field name made lowercase.   
    #tallas = models.ManyToManyField(Talla)
    tallas = ChainedManyToManyField(
        Talla,
        horizontal=True,
        verbose_name='tallas',
        chained_field="modulo_idmodulo",
        chained_model_field="modulo_idmodulo")
    slug = models.SlugField(max_length=255, blank=True)

    class Meta:
        managed = True
        db_table = 'Producto'


    def __str__(self):
        # return "name" from translation
        return self.nombre


    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.idproducto) + '-' + self.nombre)
        super(Producto, self).save(*args, **kwargs)


class Carrito(models.Model):
    idcarrito = models.AutoField(db_column='idCarrito', primary_key=True)  # Field name made lowercase.
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Carrito'

class Carritohasproductos(models.Model):
    idcarritohasproductos = models.AutoField(db_column='idCarritoHasProductos', primary_key=True)  # Field name made lowercase.
    subtotal = models.IntegerField(db_column='Subtotal', blank=True, null=True)  # Field name made lowercase.
    cantidad = models.IntegerField(db_column='Cantidad', blank=True, null=True)  # Field name made lowercase.    
    talla = models.CharField(db_column='Talla', max_length=45, blank=True, null=True)  # Field name made lowercase.
    carrito_idcarrito = models.ForeignKey(Carrito, models.CASCADE, db_column='Carrito_idCarrito')  # Field name made lowercase.
    producto_idproducto = models.ForeignKey('Producto', models.CASCADE, db_column='Producto_idProducto')  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'CarritoHasProductos'
        unique_together = (('idcarritohasproductos', 'carrito_idcarrito', 'producto_idproducto'),)

    def inventario(self):
        id_talla = Talla.objects.get(nombre=self.talla,modulo_idmodulo=self.producto_idproducto.modulo_idmodulo)
        almacen = Almacen.objects.get(producto_idproducto=self.producto_idproducto.idproducto,talla_idtalla=id_talla)
        return almacen.stock



class Delivery(models.Model):
    iddelivery = models.AutoField(db_column='idDelivery', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    precio = models.IntegerField(db_column='Precio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Delivery'

    def __str__(self):
        # return "name" from translation
        return '%s - $ %s' %(self.nombre,self.precio)


class Pedido(models.Model):
    idpedido = models.AutoField(db_column='idPedido', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Dirección', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comuna = models.CharField(db_column='Comuna', max_length=255, blank=True, null=True)
    ciudad = models.CharField(db_column='Ciudad', max_length=255, blank=True, null=True)
    delivery_iddelivery = models.ForeignKey(Delivery, models.CASCADE, db_column='Delivery_idDelivery')  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pedido = models.TextField(db_column='Pedido', blank=True, null=True)  # Field name made lowercase.
    notas = models.TextField(db_column='Notas', blank=True, null=True)  # Field name made lowercase.
    estado = models.CharField(db_column='Estado', max_length=45, blank=True, null=True)
    total = models.IntegerField(db_column='Total', blank=True, null=True)  # Field name made lowercase.
    total_delivery = models.IntegerField(db_column='Total Delivery', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    rut = models.CharField(db_column='RUT', max_length=45, blank=True, null=True)  # Field name made lowercase.
    razonsocial = models.CharField(db_column='Razon Social', max_length=150, blank=True, null=True)  # Field name made lowercase.
    industria = models.CharField(db_column='Industria', max_length=150, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'Pedido'
        unique_together = (('idpedido', 'delivery_iddelivery'),)


class Cliente(models.Model):
    idcliente = models.AutoField(db_column='idCliente', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=45, blank=True, null=True)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Dirección', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comuna = models.CharField(db_column='Comuna', max_length=255, blank=True, null=True)
    ciudad = models.CharField(db_column='Ciudad', max_length=255, blank=True, null=True)
    user = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'Cliente'


class ClientePrueba(models.Model):
    idcliente = models.AutoField(db_column='idCliente', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(db_column='Nombre', max_length=45, blank=True, null=True)  # Field name made lowercase.
    apellido = models.CharField(db_column='Apellido', max_length=45, blank=True, null=True)  # Field name made lowercase.
    contrasena = models.CharField(db_column='Contrasena', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True, null=True)  # Field name made lowercase.
    telefono = models.CharField(db_column='Telefono', max_length=45, blank=True, null=True)  # Field name made lowercase.
    direccion = models.CharField(db_column='Dirección', max_length=255, blank=True, null=True)  # Field name made lowercase.
    user = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Cliente'


class IntegracionPago(models.Model):
    STATUS_CHOICES =[(1, "Mercado Pago"), (2, "FlowCL")]
    idintegrapago = models.AutoField(db_column='idDelivery', primary_key=True)  # Field name made lowercase.
    metodo_pago = models.IntegerField(choices=STATUS_CHOICES, default=1)   
    #metodo_pago = models.CharField(db_column='Secretkey', max_length=100, null=True)  # Field name made lowercase.
    mp_public_key = models.CharField(db_column='mp_public_key', max_length=255, null=True)  # Field name made lowercase.
    mp_access_token = models.CharField(db_column='mp_access_token', max_length=255, null=True)  # Field name made lowercase.
    fw_secretkey = models.CharField(db_column='fw_secretkey', max_length=255, null=True)  # Field name made lowercase.
    fw_apiKey = models.CharField(db_column='fw_apiKey', max_length=255, null=True)  # Field name made lowercase.
    fw_url = models.CharField(db_column='fw_url', max_length=100, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'IntegracionPago'


#---------------------------------------------------------
#----------------------CONTROL STOCK----------------------
#---------------------------------------------------------

class Almacen(models.Model):
    idalmacen = models.AutoField(db_column='idalmacen', primary_key=True)
    modulo_idmodulo = models.ForeignKey(Modulo, models.CASCADE, db_column='modulo_idmodulo')
    producto_idproducto = models.ForeignKey(Producto, models.CASCADE, db_column='producto_idproducto')
    talla_idtalla = models.ForeignKey(Talla, models.CASCADE, db_column='talla_idtalla')
    stock = models.IntegerField(db_column='Stock')
    
    class Meta:
        managed = True
        db_table = 'Almacen'

    def on_transaction_commit(func):
        def inner(*args, **kwargs):
            transaction.on_commit(lambda: func(*args, **kwargs))
        return inner


    @receiver(post_save, sender=Producto)
    @on_transaction_commit
    def create_stock(sender, instance, created, **kwargs):
        producto=instance
        #print(instance.categoria_idcategoria.idcategoria)
        #print(created)
        #print(instance.tallas.all())
        #print(len(instance.tallas.all()))
        #------------------------------
        modulo=Modulo.objects.get(idmodulo=instance.modulo_idmodulo.idmodulo) 
        #print(modulo)
        stock_producto_tallas = Almacen.objects.filter(modulo_idmodulo=modulo,producto_idproducto = instance)
        stock_producto_form =instance.tallas.all()
        #print(stock_producto_tallas)
        for t in stock_producto_tallas:
            flag_exist = False
            for t2 in stock_producto_form:
                if t.talla_idtalla.idtalla ==t2.idtalla:
                    flag_exist =True
            if flag_exist :
                print("encontrado")
            else :
                print("no encontrado")
                t.delete()

        #------------------------------
        for t in stock_producto_form:                 
            talla=Talla.objects.get(idtalla=t.idtalla)             
            stock_producto = Almacen.objects.filter(modulo_idmodulo=modulo,producto_idproducto = instance, talla_idtalla = talla)
            print(stock_producto)
            print(len(stock_producto))
            if len(stock_producto) == 0:
                stock=Almacen(modulo_idmodulo=modulo,producto_idproducto=producto,talla_idtalla=talla,stock=0)
                stock.save()            

        # write you functionality    
        # pass