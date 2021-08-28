from django.contrib import admin
from .models import *
# Register your models here.

class SomeModelAdmin(admin.ModelAdmin):
    filter_horizontal = ('public',)



admin.site.register(Conference)
admin.site.register(People)
admin.site.register(Talk,SomeModelAdmin)