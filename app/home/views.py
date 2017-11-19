# -*- coding: utf-8 -*-

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView,UpdateView
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import RedirectView
from django.http import HttpResponseRedirect
from collections import OrderedDict
from django.views.generic import TemplateView
from django.core import serializers
from django.http import HttpResponse
import json
import time	

def index(request):
	nombreUser = str(request.user.first_name.encode('utf-8')) + " " + str(request.user.last_name.encode('utf-8'))

	user = request.user.rol
	if user == 1:
		return render(request,'index_administrador.html', {'nombreUser':nombreUser})
	else:
		return render(request,'index.html', {'nombreUser':nombreUser})

