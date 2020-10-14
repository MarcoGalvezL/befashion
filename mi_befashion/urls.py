from django.urls import path
from . import views

urlpatterns=[

	path('', views.index, name='index'),
	#path('Accesories/', views.index, name='index'),	
	#----	
	#path('nosotros/',views.sobre_nosotros, name='sobre_nosotros'),
	#path('productos/',views.productos,name='productos'),
	#path('item/',views.item,name='item'),
	path('add_carrito/',views.add_carrito,name='add_carrito'),
	path('carrito/',views.carrito,name='carrito'),
	path('del_carrito/',views.del_carrito,name='del_carrito'),

	path('realizar_pedido/',views.realizar_pedido,name='realizar_pedido'),
	path('realizar_pedido_factura/',views.realizar_pedido_factura,name='realizar_pedido_factura'),

	path('realizar_pedido2/',views.realizar_pedido2,name='realizar_pedido2'),		
	#path('contacto/',views.contacto,name='contacto'),			
	path('compra_exito/',views.compra_exito,name='exito'),
	path('compra_fallo/',views.compra_fallo,name='fallo'),
	path('compra_proceso/',views.compra_proceso,name='proceso'),
	#LOGIN
	path('login/',views.login_view,name='login_view'),
	path('log_out/',views.logoutView, name='logoutView'),
	path('add_user/',views.add_user,name='add_user'),
	path('user_added/',views.user_added,name='user_added'),
	path('change_pass/',views.change_pass,name='change_pass'),
	path('forgot/',views.forgot,name='forgot'),
	path('forgot2/',views.forgot2,name='forgot2'),
]