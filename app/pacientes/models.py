# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from app.pacientes.choices import *
from app.usuarios.models import Usuarios
from django.db import models

# Create your models here.

class Alumno(models.Model):
	nombres = models.CharField(max_length=50)
	direccion = models.CharField(max_length=100)
	grado = models.IntegerField(choices=grado_choices, default=1)
	edad = models.IntegerField()
	genero = models.IntegerField(choices=genero_choices, default=1)
	fecha_nacimiento = models.DateField()
	fecha_hora_creacion = models.DateTimeField()
	responsable = models.CharField(max_length=100)
	telefono = models.CharField(max_length=8)

	db_table = "Alumno"

	def __unicode__(self):
		return '{} {}'.format(self.nombres)


class Expediente(models.Model):
	alumno = models.OneToOneField(Alumno, null=True, blank=True, on_delete=models.CASCADE)
	cod_expediente = models.CharField(max_length=7,null=True, blank=True)
	responsable = models.CharField(max_length=100,null=True, blank=True)
	telefono = models.CharField(max_length=8,null=True, blank=True)
	tipo_sangre = models.CharField(max_length=10,null=True, blank=True)
	alergias = models.CharField(max_length=500,null=True, blank=True)
	enfermedades_padecidas = models.CharField(max_length=500,null=True, blank=True)
	usuario_creador = models.CharField(max_length=100,null=True, blank=True)
	fecha_hora_creacion = models.DateTimeField()


	db_table = "Expediente"

	def __unicode__(self):
		return '{}'.format(self.cod_expediente)

class Enfermedades(models.Model):
	nombre_enfermedad = models.CharField(max_length=100)

	db_table = "Enfermedades"

	def __unicode__(self):
		return '{}'.format(self.nombre_enfermedad)

class Consulta(models.Model):
	cod_expediente = models.ForeignKey(Expediente,null=False, blank=False, on_delete=models.CASCADE)
	diagnostico = models.CharField(max_length=500)
	observaciones = models.CharField(max_length=500,null=True,blank=True)
	nombre_medico = models.CharField(max_length=100)
	fecha_consulta = models.DateField()
	hora_consulta = models.TimeField()
	fecha_hora_creacion = models.DateTimeField()
	enfermedades = models.ManyToManyField(Enfermedades,null=True,blank=True)
	otras_enfermedades = models.CharField(max_length=100,null=True,blank=True)

	db_table = "Consulta"

	def __unicode__(self):
		return '{}'.format(self.cod_expediente)

class Cita(models.Model):
	consulta = models.ForeignKey(Consulta,null=False, blank=False, on_delete=models.CASCADE)
	fecha_cita = models.DateField()
	hora_cita = models.TimeField()
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Cita"

	def __unicode__(self):
		return '{}'.format(self.fecha_cita)

class Incapacidades(models.Model):
	consulta = models.ForeignKey(Consulta,null=False, blank=False, on_delete=models.CASCADE)
	motivo = models.CharField(max_length=500)
	nombre_doctor = models.CharField(max_length=100)
	num_dias = models.IntegerField()
	fecha_emision = models.DateField()
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Incapacidades"

	def __unicode__(self):
		return '{}'.format(self.fecha_emision)

class Referencias(models.Model):
	consulta = models.ForeignKey(Consulta,null=False, blank=False, on_delete=models.CASCADE)	
	centro_salud_referido = models.CharField(max_length=100)
	nombre_salud_referido = models.CharField(max_length=100)
	nombre_medico_referido = models.CharField(max_length=100)
	nombre_medico_creacion = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=500)
	fecha_referencia = models.DateField()
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Referencias"
	
	def __unicode__(self):
		return '{}'.format(self.fecha_referencia)

class Recetas(models.Model):
	consulta = models.ForeignKey(Consulta,null=False, blank=False, on_delete=models.CASCADE)
	medicamento = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=500)
	cantidad = models.IntegerField()
	fecha_receta = models.DateField()
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Recetas"
	
	def __unicode__(self):
		return '{}'.format(self.fecha_receta)

class Casos_embarazos(models.Model):
	consulta = models.ForeignKey(Consulta,null=False,blank=False,on_delete=models.CASCADE)
	numero_meses = models.IntegerField()
	genero_feto = models.IntegerField(choices=genero_choices, default=1)
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Casos_embarazos"

	def __unicode__(self):
		return '{}'.format(self.fecha_hora_creacion)


class Tipo_actividad(models.Model):
	nombre_actividad = models.CharField(max_length= 100)
	fecha_actividad = models.DateField()
	descripcion_actividad = models.CharField(max_length=500)
	fecha_hora_creacion = models.DateTimeField()

	db_table = "Tipo_actividad"

	def __unicode__(self):
		return '{}'.format(self.nombre_actividad)

class Actividad(models.Model):
	desarrolla_por = models.CharField(max_length=100)
	descripcion = models.CharField(max_length=500)

	db_table = "Actividad"

	def __unicode__(self):
		return '{}'.format(self.desarrolla_por)





