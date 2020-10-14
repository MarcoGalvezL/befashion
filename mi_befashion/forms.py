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

	nombre = forms.CharField(label=False,widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Nombre'
		}),required=True)

	email = forms.EmailField(label=False,widget=forms.EmailInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Email'
		}),required=True)

	telefono = forms.CharField(label=False,widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Teléfono'
		}),required=True)

	direccion = forms.CharField(label=False,widget=forms.TextInput(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Direccion'
		}),required=True)

	delivery = forms.ModelChoiceField(queryset=Delivery.objects.all(),label=False, widget=forms.Select(attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Delivery'
		}), required=True)

	notas = forms.CharField(label=False,widget=forms.Textarea(
		attrs={
			'class':'form-control display-7 form-group',
			'placeholder': 'Notas',
			'rows':3,
		}))


