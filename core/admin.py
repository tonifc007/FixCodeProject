# -*- coding: utf 8 -*-
from django.contrib import admin
from .models import Fixies, ComentFixies, Participations, Favorites

# Register your models here.

admin.site.register(Fixies)
admin.site.register(ComentFixies)
admin.site.register(Participations)
admin.site.register(Favorites)