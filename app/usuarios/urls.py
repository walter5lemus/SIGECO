from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required
from app.usuarios.views import *

urlpatterns = [
   url(r'^gestion/$', login_required(gestion_usuarios), name='gestion_usuarios'),
   url(r'^registrar/$', login_required(RegistroUsuario.as_view()), name='RegistroUsuario'),
   url(r'^desactivar/', login_required(Desactivar_user), name= 'Desactivar_user'),
   url(r'^backupBD/$', login_required(backupRestoreBD), name='backupRestoreBD'),
   url(r'^backupRestore/$', login_required(backupRestore), name='backupRestore'),
   url(r'^restoreBD/$', login_required(restoreBD), name='restoreBD'),

]