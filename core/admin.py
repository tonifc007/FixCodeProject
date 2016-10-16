# -*- coding: utf 8 -*-
from django.contrib import admin
from .models import Fixies, ComentFixies, Participations, Favorites, Profile, Followers, Post, Areas

# Register your models here.

admin.site.register(Fixies)
admin.site.register(ComentFixies)
admin.site.register(Participations)
admin.site.register(Favorites)
admin.site.register(Profile)
admin.site.register(Followers)
admin.site.register(Post)
admin.site.register(Areas)