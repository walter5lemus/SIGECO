# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from app.pacientes.forms import *
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,UpdateView,ListView,TemplateView
from django.http import HttpResponse,HttpResponseRedirect,HttpResponse
from django.views.generic.base import RedirectView
from collections import OrderedDict
from django.core import serializers
import json
from django.db.models import Q
import datetime


# Create your views here.

def home(request):
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	
	return HttpResponseRedirect('/pacientes/alumno/crear/')

def alumno_crear(request):
	user = request.user.id
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	fecha =  timezone.now()
	if request.method == 'POST':
			form = Alumno_form(request.POST)
			if form.is_valid():	
			 	form.save()							
				return HttpResponseRedirect('/pacientes/expediente/crear/')
			else:
				return render(request, 'pacientes/alumno_crear.html', {'form':form,'nombreUser':nombreUser})
	else:
		form = Alumno_form(initial={'fecha_hora_creacion':fecha})
		return render(request, 'pacientes/alumno_crear.html', {'form':form,'nombreUser':nombreUser})

def alumno_consultar(request,):
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	fecha =  timezone.now()
	user = request.user.rol
	form = Alumno_form_consultar(initial={'fecha_hora_creacion':fecha})
	form2 = Expediente_form_consultar(initial={'fecha_hora_creacion':fecha})
	return render(request, 'pacientes/alumno_consultar.html', {'form':form,'form2':form2,'nombreUser':nombreUser,'user':user})

def alumno_editar(request,num):
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	if request.user.rol==1:
		datos = Alumno.objects.get(id=num)
		if request.method == 'GET':
			form = Alumno_form(instance=datos)
		else: 
			form = Alumno_form(request.POST, instance=datos)
			if form.is_valid():
				form.save()
				return HttpResponseRedirect('/pacientes/alumno/consultar/')
		return render(request,'pacientes/alumno_editar.html',{'form':form,'nombreUser':nombreUser})

	else:
		return HttpResponseRedirect('/')

########################################################################################################################
def expediente_crear(request):
	user = request.user.id
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	fecha =  timezone.now()
	if request.method == 'POST':
		form = Expediente_form(request.POST)
		if form.is_valid():	
			 	form.save()
			 	return HttpResponseRedirect('/pacientes/consulta/crear/')
		else:
			return render(request, 'pacientes/expediente_crear.html', {'form':form,'nombreUser':nombreUser})
	else:
		form = Expediente_form(initial={'fecha_hora_creacion':fecha})
		return render(request, 'pacientes/expediente_crear.html', {'form':form,'nombreUser':nombreUser})


def consulta_crear(request):
	user = request.user.id
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	fecha =  timezone.now()
	if request.method == 'POST':
		form = Consulta_form(request.POST)
		if form.is_valid():	
			 	form.save()
			 	return HttpResponseRedirect('/')
		else:
			return render(request, 'pacientes/consulta_crear.html', {'form':form,'nombreUser':nombreUser})
	else:
		form = Consulta_form(initial={'fecha_hora_creacion':fecha})
		return render(request, 'pacientes/consulta_crear.html', {'form':form,'nombreUser':nombreUser})

def consulta_consultar(request):
	user = request.user.id
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))
	fecha =  timezone.now()
	form = Consulta_form_consultar(initial={'fecha_hora_creacion':fecha})
	return render(request, 'pacientes/consulta_consultar.html', {'form':form,'nombreUser':nombreUser})



############################################################################################################################

def busqueda(request):
	if request.is_ajax():
		resultado = Alumno.objects.filter(nombres__istartswith=request.GET['nombre'])
		for resul in resultado:
			resul.fecha_nacimiento.strftime('%m/%d/%Y')
		data = serializers.serialize('json', resultado, fields=('nombres', 'apellidos','direccion','grado','genero','responsable','telefono','fecha_nacimiento'))
		return HttpResponse(data, content_type='application/json')

class BusquedaAjaxView(TemplateView):
	def get(self,request,*args,**kwargs):
		codigo = request.GET['id_pk']
		fi=list(Expediente.objects.filter(alumno_id=codigo))
		data = serializers.serialize('json', fi, fields=('cod_expediente'))
		return HttpResponse(data, content_type='application/json')

def busqueda_expediente(request):
	if request.is_ajax():
		resultado = Consulta.objects.filter(cod_expediente__cod_expediente__istartswith=request.GET['codigo']).values('cod_expediente').distinct()
		id_expediente = Expediente.objects.filter(id=resultado)
		data = serializers.serialize('json', id_expediente, fields=('cod_expediente'))
		return HttpResponse(data, content_type='application/json')

def busqueda_consulta(request):
	if request.is_ajax():
		resultado = Consulta.objects.filter(cod_expediente__cod_expediente__istartswith=request.GET['codigo']).values('cod_expediente').distinct()
		consultas = Consulta.objects.filter(id=resultado)
		data = serializers.serialize('json', consultas, fields=('fecha_consulta','diagnostico','observaciones','nombre_medico','hora_consulta'))
		return HttpResponse(data, content_type='application/json')


