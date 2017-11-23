# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.core.urlresolvers import reverse_lazy
from django.core.management import call_command
from django.http import HttpResponse,HttpResponseRedirect,HttpResponse
from app.usuarios.forms import *
from app.usuarios.models import *
from django.contrib.auth import get_user_model
import sys
import os
# Create your views here.

def gestion_usuarios(request):
	user = request.user.rol
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	listaUsuarios = Usuarios.objects.all().order_by("pk")
	for usuario in listaUsuarios:
		if usuario.rol == 1:
			usuario.rol = "Administrador" 
		elif usuario.rol == 2:
			usuario.rol = "Doctor"
		elif usuario.rol == 3:
			usuario.rol = "Asistente"
		if usuario.is_active == True:
			usuario.is_active = "Activo"
		elif usuario.is_active == False:
			usuario.is_active = "Desactivado"
	if user == 1:
		return render(request,'usuarios/gestion_usuarios.html', {'user':user,'nombreUser':nombreUser,'listaUsuarios':listaUsuarios})
	else:
		return HttpResponseRedirect('/')

def backupRestore(request):
	user = request.user.rol
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	if user == 1:
		return render(request,'usuarios/backuprestore.html', {'user':user,'nombreUser':nombreUser})
	else:
		return HttpResponseRedirect('/')

class RegistroUsuario(CreateView):
	model = get_user_model()
	template_name = "usuarios/registrar.html"
	form_class = RegistroForm
	#success_url = reverse_lazy('usuarios:gestion_usuarios')

	def post(self, request,*args, **kwargs):
		form = self.form_class(request.POST)
		args = {}

		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/usuarios/gestion/')
		else:
			args['form'] = form
			return render(request,'usuarios/registrar.html',args)
		return render(request,'usuarios/gestion_usuarios.html',args)

def Desactivar_user(request):
	id_user = request.POST['id']
	if request.user.rol == 1:
		if request.method == 'POST':
			if Usuarios.objects.filter(id=id_user).exists():
				Usuarios.objects.filter(id=id_user).update(is_active=0)
				return HttpResponse('<script>alert("Se desactivo correctamente");</script>')
			else:
				return HttpResponse('Error', status=401)
		return HttpResponse('Error', status=401)
	else: 
		return HttpResponse('Error', status=401)

def backupRestoreBD(request):
	user = request.user.rol
	fecha =  timezone.now().strftime("%d_%m_%Y_%H_%M_%S")
	if user == 1:
		if request.method == 'GET':
			#filename = open(os.path.join('folder','filename.txt'),'w')
			sys.stdout = open(os.path.join('backups',str(fecha)+'.json'), 'w')
			call_command('dumpdata')
			return render(request, 'usuarios/gestion_usuarios.html')
		else:
			return HttpResponse('Error', status=401)
	else:
		return HttpResponse('Error', status=401)

def backupRestoreBD(request):
	user = request.user.rol
	fecha =  timezone.now().strftime("%d_%m_%Y_%H_%M_%S")
	if user == 1:
		if request.method == 'GET':
			#filename = open(os.path.join('folder','filename.txt'),'w')
			sys.stdout = open(str(fecha)+'.json', 'w')
			call_command('dumpdata', e=["usuarios.usuarios","auth.permission"])
			sys.stdout.close()
			return render(request, 'usuarios/gestion_usuarios.html')

		else:
			return HttpResponse('Error', status=401)
	else:
		return HttpResponse('Error', status=401)

def restoreBD(request):
	user = request.user.rol
	name = request.POST['nombre']
	if user == 1:
		if request.method == 'POST':
			call_command('loaddata', name)
			return render(request, 'usuarios/gestion_usuarios.html')

		else:
			return HttpResponse('Error', status=401)
	else:
		return HttpResponse('Error', status=401)