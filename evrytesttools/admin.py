from django.contrib import admin
from .models import VIORecord,QuerySRRecord,QueryCMDBRecord,SRCreateServerLinuxRecord,LinuxInfoRecord,RundeckRecord,EndtoendRecord
# Register your models here.

class VIORecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','instancename','imagename','ip','size','status','availabilityzone','powerstate')

admin.site.register(VIORecord,VIORecordAdmin)

class QuerySRRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','sr','summary','hostname','ip','status')

admin.site.register(QuerySRRecord,QuerySRRecordAdmin)

class QueryCMDBRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','hostname','name','tshirtsize','operationalstatus','numcpus','memorysize','model')

admin.site.register(QueryCMDBRecord,QueryCMDBRecordAdmin)

class SRCreateServerLinuxRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','hostname','tshirtsize','vcpusize','memsize','hypervisor','securityzone','srsubmitedinfo','operationusername')

admin.site.register(SRCreateServerLinuxRecord,SRCreateServerLinuxRecordAdmin)

class LinuxInfoRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','Hostname','IP','CPUnumber','MEM','Disk','InstancePassword','logfilepath','hypervisortogetpassword','customertogetpassword')

admin.site.register(LinuxInfoRecord,LinuxInfoRecordAdmin)

class RundeckRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','icdDispatcherJobID','icdDispatcherJobStatus','icdDispatcherJobDuration','workorderid','privatecloudJobID','privatecloudJobStatus','privatecloudJobDuration')

admin.site.register(RundeckRecord,RundeckRecordAdmin)

class EndtoendRecordAdmin(admin.ModelAdmin):
    list_display = ('id','date','endtoendID','createSRID','querySRID','cmdbID','vioID','rundeckID','linuxinstanceID')

admin.site.register(EndtoendRecord,EndtoendRecordAdmin)