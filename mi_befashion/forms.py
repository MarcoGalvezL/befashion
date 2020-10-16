from django import forms
from django.db import models
from django.forms import ModelForm

#Crispy forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

#importar modelos..
from .models import *
from django.contrib.auth.models import User

class Formulario_Crear_Nuevo(forms.Form):

	nombre = forms.CharField(label='Nombre',widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Nombre'
		}),required=True)

	email = forms.EmailField(label='Email',widget=forms.EmailInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Email'
		}),required=True)

	telefono = forms.CharField(label='Telefono',widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Teléfono'
		}),required=True)

	direccion = forms.CharField(label='Direccion',widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Direccion'
		}),required=True)

	comuna = forms.CharField(label='Comuna',widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Comuna'
		}),required=True)
	ciudad = forms.CharField(label='Ciudad',widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Ciudad'
		}),required=True)

	delivery = forms.ModelChoiceField(queryset=Delivery.objects.all(),label='Selecciona una opcion de delivery', widget=forms.Select(attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Delivery'
		}), required=True)

	notas = forms.CharField(label='notas',widget=forms.Textarea(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Notas',
			'rows':3,
		}))


