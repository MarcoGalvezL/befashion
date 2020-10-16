from django.contrib import admin
from mi_befashion.models import *
from django.utils.html import mark_safe

# Register your models here.



class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre','descripcion')
    search_fields = ('nombre', 'descripcion')
admin.site.register(Modulo,ModuloAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('modulo_idmodulo','nombre','descripcion')
    search_fields = ('nombre', 'descripcion')
admin.site.register(Categoria,CategoriaAdmin)

class MarcaAdmin(admin.ModelAdmin):
    list_display = ('modulo_idmodulo','nombre','image_tag')
    search_fields = ('nombre',)
admin.site.register(Marca,MarcaAdmin)

class TallaAdmin(admin.ModelAdmin):
    list_display = ('modulo_idmodulo','nombre')
    search_fields = ('modulo_idmodulo','nombre')
admin.site.register(Talla,TallaAdmin)

class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre','idproducto','short','destacado','precio')
    list_filter = ('destacado', 'modulo_idmodulo','promocion','preventa','activo',)
    search_fields = ('nombre', 'short', 'descripcion','idproducto', )
    #filter_horizontal = ('tallas',)

admin.site.register(Producto,ProductoAdmin)
#------

class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('nombre','precio')
    search_fields = ('nombre', 'short', 'descripcion','idproducto', )

admin.site.register(Delivery,DeliveryAdmin)

class PedidoAdmin(admin.ModelAdmin):
    list_display = ('idpedido','nombre', 'direccion', 'telefono','estado','total','total_delivery')
    list_filter = ('estado',)
    search_fields = ('idpedido','nombre',)

admin.site.register(Pedido,PedidoAdmin)

class CarritoAdmin(admin.ModelAdmin):
    list_display = ('idcarrito','total')
    search_fields = ('idcarrito',) 

admin.site.register(Carrito,CarritoAdmin)

class CarritoHasProductosAdmin(admin.ModelAdmin):
    list_display = ('idcarritohasproductos','subtotal')
    search_fields = ('idcarritohasproductos',) 

admin.site.register(Carritohasproductos,CarritoHasProductosAdmin)

class IntegracionPagoAdmin(admin.ModelAdmin):
    list_display = ('metodo_pago',)
    search_fields = ('metodo_pago',) 

admin.site.register(IntegracionPago,IntegracionPagoAdmin)

class AlmacenPagoAdmin(admin.ModelAdmin):    
    list_display = ('modulo_idmodulo','producto_idproducto','talla_idtalla','stock')    
    readonly_fields = ('modulo_idmodulo', 'producto_idproducto','talla_idtalla')
    list_filter = ('talla_idtalla','stock','modulo_idmodulo',)
admin.site.register(Almacen,AlmacenPagoAdmin)

