	# -*- coding: utf-8 -*-
from django import forms
from app.usuarios.models import *
from django.contrib.admin import widgets
from datetime import datetime
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError 
from django.contrib.auth import get_user_model

class RegistroForm(UserCreationForm):

	class Meta:
		model= get_user_model()
		fields = [
			'username',
			'first_name',
			'last_name',
			'email',
			'rol'
		]
		labels = {
			'username': 'Nombre de Usuario',
			'first_name':'Nombre',
			'last_name': 'Apellido',
			'email':'Correo',
			'rol':'Rol del Usuario',
		}



