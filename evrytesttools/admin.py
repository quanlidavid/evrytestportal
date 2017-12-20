from django.contrib import admin
from .models import VIORecord,QuerySRRecord,QueryCMDBRecord,SRCreateServerLinuxRecord,LinuxInfoRecord
# Register your models here.

class VIORecordAdmin(admin.ModelAdmin):
    list_display = ('date','instancename','imagename','ip','size','status','availabilityzone','powerstate')

admin.site.register(VIORecord,VIORecordAdmin)

class QuerySRRecordAdmin(admin.ModelAdmin):
    list_display = ('date','sr','summary','hostname','ip','status')

admin.site.register(QuerySRRecord,QuerySRRecordAdmin)

class QueryCMDBRecordAdmin(admin.ModelAdmin):
    list_display = ('date','hostname','name','tshirtsize','operationalstatus','numcpus','memorysize','model')

admin.site.register(QueryCMDBRecord,QueryCMDBRecordAdmin)

class SRCreateServerLinuxRecordAdmin(admin.ModelAdmin):
    list_display = ('date','hostname','tshirtsize','vcpusize','memsize','hypervisor','securityzone','srsubmitedinfo','operationusername')

admin.site.register(SRCreateServerLinuxRecord,SRCreateServerLinuxRecordAdmin)

class LinuxInfoRecordAdmin(admin.ModelAdmin):
    list_display = ('date','Hostname','IP','CPUnumber','MEM','Disk','InstancePassword','logfilepath','hypervisortogetpassword','customertogetpassword')

admin.site.register(LinuxInfoRecord,LinuxInfoRecordAdmin)