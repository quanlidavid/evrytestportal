from django.contrib import admin
from .models import VIOinfo,QuerySRRecord,QueryCMDBRecord,SRCreateServerLinuxRecord
# Register your models here.

class VIOinfoAdmin(admin.ModelAdmin):
    list_display = ('instancename','imagename','ip','size')

admin.site.register(VIOinfo,VIOinfoAdmin)

class QuerySRRecordAdmin(admin.ModelAdmin):
    list_display = ('date','sr','summary','hostname','ip','status')

admin.site.register(QuerySRRecord,QuerySRRecordAdmin)

class QueryCMDBRecordAdmin(admin.ModelAdmin):
    list_display = ('date','hostname','name','tshirtsize','operationalstatus','numcpus','memorysize','model')

admin.site.register(QueryCMDBRecord,QueryCMDBRecordAdmin)

class SRCreateServerLinuxRecordAdmin(admin.ModelAdmin):
    list_display = ('date','hostname','tshirtsize','vcpusize','memsize','hypervisor','securityzone','srsubmitedinfo')

admin.site.register(SRCreateServerLinuxRecord,SRCreateServerLinuxRecordAdmin)