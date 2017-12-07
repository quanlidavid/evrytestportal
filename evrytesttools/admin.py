from django.contrib import admin
from .models import VIOinfo,QuerySRRecord
# Register your models here.

class VIOinfoAdmin(admin.ModelAdmin):
    list_display = ('instancename','imagename','ip','size')

admin.site.register(VIOinfo,VIOinfoAdmin)

class QuerySRRecordAdmin(admin.ModelAdmin):
    list_display = ('sr','summary','hostname','ip','status')

admin.site.register(QuerySRRecord,QuerySRRecordAdmin)