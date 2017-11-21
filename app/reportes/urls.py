from django.conf.urls import url,include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from app.reportes.views import *

urlpatterns = [
	url(r'^pacientes_atendidos/$', login_required(index_pacientes_atendidos), name='index_pacientes_atendidos'),
	url(r'^enfermedades_frecuentes/$', login_required(index_enfermedades_frecuentes), name='index_enfermedades_frecuentes'),
	url(r'^frecuencia_consultas/$', login_required(index_frecuencias_consultas), name='index_frecuencias_consultas'),

	url(r'^reporte_pacientes_atendidos/(?P<fecha>[^/]+)/(?P<fecha2>[^/]+)/$', login_required(Reporte1.as_view()), name='generar_pdf_1'),
	url(r'^reporte_enfermedades_frecuentes/(?P<fecha>[^/]+)/(?P<fecha2>[^/]+)/$', login_required(Reporte2.as_view()), name='generar_pdf_2'),
	url(r'^reporte_frecuencia_consultas/(?P<fecha>[^/]+)/(?P<fecha2>[^/]+)/$', login_required(Reporte3.as_view()), name='generar_pdf_3'),

]