from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.pacientes.views import *



urlpatterns = [
   url(r'^$', login_required(home), name='home'),
   url(r'alumno/crear/$', login_required(alumno_crear), name='alumno_crear'),
   url(r'alumno/consultar/$', login_required(alumno_consultar), name='alumno_consultar'),
   url(r'alumno/editar/(?P<num>\d+)/$', login_required(alumno_editar),name='alumno_editar'),


   url(r'expediente/crear/$', login_required(expediente_crear), name='expediente_crear'),
#   url(r'expediente/editar/$', login_required(expediente_editar), name='expediente_editar'),


   url(r'consulta/crear/$', login_required(consulta_crear), name='consulta_crear'), 
   url(r'consulta/consultar/$', login_required(consulta_consultar), name='consulta_consultar'), 


   url(r'^busqueda/$', login_required(busqueda), name='busquedaNombre'),
   url(r'^busqueda_idExpediente/$', login_required(busqueda_idExpediente), name='busqueda_idExpediente'),
   url(r'^busqueda2/$', login_required(BusquedaAjaxView.as_view()), name='BusquedaAjaxView'),
   url(r'^busqueda_expediente/$', login_required(busqueda_expediente), name='busqueda_expediente'),
   url(r'^busqueda_consulta/$', login_required(busqueda_consulta), name='busqueda_consulta'),


]   