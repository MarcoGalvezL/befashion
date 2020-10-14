from django.urls import path
from . import views

urlpatterns=[

	path('', views.index, name='index'),
	path('productos/',views.productos,name='productos'),
	path('item/<str:producto>/',views.item,name='item'),
	path('nosotros/',views.sobre_nosotros, name='sobre_nosotros'),
]