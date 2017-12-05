from django.contrib import admin
from .models import VIOinfo
# Register your models here.

class VIOinfoAdmin(admin.ModelAdmin):
    list_display = ('instancename','imagename','ip','size')

admin.site.register(VIOinfo,VIOinfoAdmin)