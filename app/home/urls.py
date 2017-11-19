from django.conf.urls import url, include
from django.contrib.auth.decorators import login_required

urlpatterns = [
   url(r'^$', login_required(index), name='home1'),
]   