	# -*- coding: utf-8 -*-
from django import forms
from app.pacientes.models import *
from django.contrib.admin import widgets
from app.pacientes.choices import *
from datetime import datetime
from datetime import date
from django.forms.extras.widgets import SelectDateWidget

class Alumno_form(forms.ModelForm):
	class Meta:
		model = Alumno
		this_year = datetime.now().year+1

		fields = [
			'nombres',
			'direccion',
			'grado',
			'edad',
			'genero',
			'fecha_nacimiento',
			'fecha_hora_creacion',
			'responsable',
			'telefono',
		]

		labels={
			'nombres':'Nombres',
			'direccion':'Dirección',
			'edad':'Edad',
			'grado':'Grado',
			'genero':'Género',
			'fecha_nacimiento':'Fecha de Nacimiento',
			'fecha_hora_creacion':'Fecha y hora de creación',
			'responsable':'Nombre del Padre o Encargado',
			'telefono':'Teléfono ',
		}

		widgets={
			'nombres':forms.TextInput(attrs={'class':'form-control'}),
			'direccion':forms.TextInput(attrs={'class':'form-control'}),
			'edad':forms.NumberInput(attrs={'class':'form-control','min':1,'readonly':True}),
			'grado':forms.Select(attrs={'class':'form-control'}),
			'genero':forms.Select(attrs={'class':'form-control'}),
			'fecha_nacimiento':forms.SelectDateWidget(years=range(1980,this_year,1),attrs={'class':'form-control fecha','style': 'width: 243px; display: inline-block;'}),
			'fecha_hora_creacion':forms.HiddenInput(attrs={'class':'form-control','readonly':'true'}),
			'responsable':forms.TextInput(attrs={'class':'form-control'}),
			'telefono':forms.TextInput(attrs={'class':'form-control'}),
		}

class Alumno_form_consultar(forms.ModelForm):
	class Meta:
		model = Alumno
		this_year = datetime.now().year+1

		fields = [
			'nombres',
			'direccion',
			'grado',
			'edad',
			'genero',
			'fecha_nacimiento',
			'fecha_hora_creacion',
			'responsable',
			'telefono',
		]

		labels={
			'nombres':'Nombres',
			'direccion':'Dirección',
			'edad':'Edad Actual',
			'grado':'Grado de registro',
			'genero':'Género',
			'fecha_nacimiento':'Fecha de Nacimiento',
			'fecha_hora_creacion':'Fecha y hora de creación',
			'responsable':'Nombre del Padre o Encargado',
			'telefono':'Teléfono ',
		}

		widgets={
			'nombres':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'direccion':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'edad':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'grado':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'genero':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'fecha_nacimiento':forms.DateInput(attrs={'class':'form-control fecha','readonly':True}),
			'fecha_hora_creacion':forms.HiddenInput(attrs={'class':'form-control','readonly':True}),		
			'responsable':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'telefono':forms.TextInput(attrs={'class':'form-control','readonly':True}),
		}

class Expediente_form(forms.ModelForm):
	class Meta:
		model = Expediente

		fields = [
			'alumno',
			'cod_expediente',
			'responsable',
			'telefono',
			'tipo_sangre',
			'alergias',
			'enfermedades_padecidas',			
			'usuario_creador',
			'fecha_hora_creacion',
		]
		labels = {
			'alumno' : 'Alumno',
			'cod_expediente':'Codigo de Expediente',
			'responsable':'Nombre del Padre o Encargado',
			'telefono':'Teléfono',
			'tipo_sangre':'Tipo de Sangre',
			'alergias':'Alergias',
			'enfermedades_padecidas':'Enfermedades Padecidas Anteriormente',
			'usuario_creador':'usuario creador',
			'fecha_hora_creacion':'Fecha y hora de creación',
		}
		widgets = {
			'alumno' : forms.HiddenInput(attrs={'class':'form-control'}),
			'cod_expediente':forms.TextInput(attrs={'class':'form-control'}),
			'responsable':forms.TextInput(attrs={'class':'form-control'}),
			'telefono':forms.TextInput(attrs={'class':'form-control', 'pattern':'[0-9]{8}','title':'Ejemplo: 77777777'}),
			'tipo_sangre':forms.TextInput(attrs={'class':'form-control'}),
			'alergias':forms.Textarea(attrs={'class':'form-control'}),
			'enfermedades_padecidas':forms.Textarea(attrs={'class':'form-control'}),
			'usuario_creador':forms.HiddenInput(attrs={'class':'form-control'}),
			'fecha_hora_creacion':forms.HiddenInput(attrs={'class':'form-control'}),
		}

class Expediente_form_consultar(forms.ModelForm):
	class Meta:
		model = Expediente

		fields = [
			'alumno',
			'cod_expediente',
			'responsable',
			'telefono',
			'tipo_sangre',
			'alergias',
			'enfermedades_padecidas',			
			'usuario_creador',
			'fecha_hora_creacion',
		]
		labels = {
			'alumno' : 'Alumno',
			'cod_expediente':'Codigo de Expediente',
			'responsable':'Nombre del Padre o Encargado',
			'telefono':'Teléfono',
			'tipo_sangre':'Tipo de Sangre',
			'alergias':'Alergias',
			'enfermedades_padecidas':'Enfermedades Padecidas Anteriormente',
			'usuario_creador':'usuario creador',
			'fecha_hora_creacion':'Fecha y hora de creación',
		}
		widgets = {
			'alumno' : forms.HiddenInput(attrs={'class':'form-control'}),
			'cod_expediente':forms.TextInput(attrs={'class':'form-control', 'pattern':'[0-9]{4}[-]{1}[0-9]{2}','title':'Ejemplo: 0001-16','readonly':True}),
			'responsable':forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'telefono':forms.TextInput(attrs={'class':'form-control', 'pattern':'[0-9]{8}','title':'Ejemplo: 77777777','readonly':True}),
			'tipo_sangre':forms.TextInput(attrs={'class':'form-control'}),
			'alergias':forms.Textarea(attrs={'class':'form-control'}),
			'enfermedades_padecidas':forms.Textarea(attrs={'class':'form-control'}),
			'usuario_creador':forms.HiddenInput(attrs={'class':'form-control','readonly':True}),
			'fecha_hora_creacion':forms.HiddenInput(attrs={'class':'form-control','readonly':True}),
		}

class Consulta_form(forms.ModelForm):
	class Meta:
		model = Consulta
		this_year = datetime.now().year+1

		fields = [
			'cod_expediente',
			'diagnostico',
			'observaciones',
			'nombre_medico',
			'fecha_consulta',
			'hora_consulta',
			'fecha_hora_creacion',
			'enfermedades',
			'otras_enfermedades',
		]
		labels = {
			'cod_expediente' : 'Codigo de Expediente',
			'diagnostico': 'Diagnostico de la consulta',
			'observaciones': 'Observaciones',
			'nombre_medico':'Nombre del Medico que atendió la consulta',
			'fecha_consulta': 'Fecha de la consulta',
			'hora_consulta':'Hora de Consulta',
			'fecha_hora_creacion': 'Fecha y hora de creación',
			'enfermedades': 'Enfermedades diagnosticadas',
			'otras_enfermedades': 'Otras enfermedades',
		}
		widgets = {
			'cod_expediente': forms.Select(attrs={'class':'form-control', 'pattern':'[0-9]{4}[-]{1}[0-9]{2}','title':'Ejemplo: 0001-16','autocomplete':'off'}),
			'diagnostico': forms.Textarea(attrs={'class':'form-control'}),
			'observaciones': forms.Textarea(attrs={'class':'form-control'}),
			'nombre_medico': forms.TextInput(attrs={'class':'form-control'}),
			'fecha_consulta': forms.TextInput(attrs={'class':'form-control'}),
			'hora_consulta' : forms.TextInput(attrs={'class':'form-control'}),
			'fecha_hora_creacion': forms.HiddenInput(attrs={'class':'form-control','readonly':True}),
			'enfermedades': forms.CheckboxSelectMultiple(attrs={'class':'lista'}),
			'otras_enfermedades': forms.TextInput(attrs={'class':'form-control'}),
		}

	"""def clean(self):

		# Sobrecargar clean devuelve un diccionario con los campos
		cleaned_data = super(Consulta_form, self).clean()
		valor_propiedad = cleaned_data.get("fecha_consulta")
     
		if valor_propiedad > date.today():
			raise forms.ValidationError({'fecha_consulta': ["La Fecha de Registro que seleccionó es mayor al dia de ahora",]})
        # Siempre hay que devolver el diccionario
		return cleaned_data"""

class Consulta_form_consultar(forms.ModelForm):
	class Meta:
		model = Consulta
		this_year = datetime.now().year+1

		fields = [
			'cod_expediente',
			'diagnostico',
			'observaciones',
			'nombre_medico',
			'fecha_consulta',
			'hora_consulta',
			'fecha_hora_creacion',
			'enfermedades',
			'otras_enfermedades',
		]
		labels = {
			'cod_expediente' : 'Codigo de Expediente',
			'diagnostico': 'Diagnostico de la consulta',
			'observaciones': 'Observaciones',
			'nombre_medico':'Nombre del Medico que atendió la consulta',
			'fecha_consulta': 'Fecha de la consulta',
			'hora_consulta':'Hora de Consulta',
			'fecha_hora_creacion': 'Fecha y hora de creación',
			'enfermedades': 'Enfermedades diagnosticadas',
			'otras_enfermedades': 'Otras enfermedades',
		}
		widgets = {
			'cod_expediente': forms.TextInput(attrs={'class':'form-control','autocomplete':'off'}),
			'diagnostico': forms.Textarea(attrs={'class':'form-control','readonly':True}),
			'observaciones': forms.Textarea(attrs={'class':'form-control','readonly':True}),
			'nombre_medico': forms.TextInput(attrs={'class':'form-control','readonly':True}),
			'fecha_consulta': forms.Select(attrs={'class':'form-control'}),
			'hora_consulta' : forms.TimeInput(attrs={'class':'form-control'}),
			'fecha_hora_creacion': forms.HiddenInput(attrs={'class':'form-control','readonly':True}),
			'enfermedades': forms.HiddenInput(attrs={'class':'lista','readonly':True}),
			'otras_enfermedades': forms.HiddenInput(attrs={'class':'form-control','readonly':True}),
		}