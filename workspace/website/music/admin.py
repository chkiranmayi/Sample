# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Album, Song


# Register your models here.

admin.site.register(Album) #to display album table in admin page
admin.site.register(Song)
