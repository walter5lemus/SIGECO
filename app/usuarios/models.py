# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.

class Usuarios(AbstractUser):
    rol = models.IntegerField(null=True, blank=True)

