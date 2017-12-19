from django.db import models


# Create your models here.
# for vio record

class VIORecordsManager(models.Manager):
    def create_VIORecord(self, instanceinfo):
        viorecord = self.create(instancename=instanceinfo['instancename'],
                                imagename=instanceinfo['imagename'],
                                ip=instanceinfo['ip'],
                                size=instanceinfo['size'],
                                status=instanceinfo['status'],
                                availabilityzone=instanceinfo['availabilityzone'],
                                powerstate=instanceinfo['powerstate'])
        return viorecord
class VIORecord(models.Model):
    date = models.DateTimeField(auto_now=True, auto_created=True)
    instancename = models.CharField(max_length=100)
    imagename = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    availabilityzone = models.CharField(max_length=100)
    powerstate = models.CharField(max_length=100)

    objects = VIORecordsManager()

    class Meta:
        ordering = ('-instancename', '-date')

    def __str__(self):
        return self.instancename


# for query sr
class QuerySRRecordsManager(models.Manager):
    def create_QuerySRRecord(self, sr_icd_info):
        querysrrecord = self.create(sr=sr_icd_info['sr'],
                                    summary=sr_icd_info['summary'],
                                    classification_description=sr_icd_info['classification_description'],
                                    status=sr_icd_info['status'],
                                    configuration_item_name=sr_icd_info['configuration_item_name'],
                                    ip=sr_icd_info['ip'],
                                    hostname=sr_icd_info['hostname'],
                                    customer=sr_icd_info['customer'],
                                    disksize=sr_icd_info['disksize'],
                                    memsize=sr_icd_info['memsize'],
                                    virtualsize=sr_icd_info['virtualsize'],
                                    cpusize=sr_icd_info['cpusize'],
                                    hypervisor=sr_icd_info['hypervisor'])
        return querysrrecord


class QuerySRRecord(models.Model):
    date = models.DateTimeField(auto_now=True, auto_created=True)
    sr = models.CharField(max_length=100)
    summary = models.CharField(max_length=100)
    classification_description = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    configuration_item_name = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    disksize = models.CharField(max_length=100)
    memsize = models.CharField(max_length=100)
    virtualsize = models.CharField(max_length=100)
    cpusize = models.CharField(max_length=100)
    hypervisor = models.CharField(max_length=100)

    objects = QuerySRRecordsManager()

    class Meta:
        ordering = ('-sr', '-date')

    def __str__(self):
        return self.sr


# for query cmdb
class QueryCMDBRecordsManager(models.Manager):
    def create_QueryCMDBRecord(self, cmdb_icd_info):
        querycmdbrecord = self.create(hostname=cmdb_icd_info['hostname'],
                                      name=cmdb_icd_info['name'],
                                      memorysize=cmdb_icd_info['memorysize'],
                                      tshirtsize=cmdb_icd_info['tshirtsize'],
                                      numcpus=cmdb_icd_info['numcpus'],
                                      operationalstatus=cmdb_icd_info['operationalstatus'],
                                      model=cmdb_icd_info['model'])
        return querycmdbrecord


class QueryCMDBRecord(models.Model):
    date = models.DateTimeField(auto_now=True, auto_created=True)
    hostname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    memorysize = models.CharField(max_length=100)
    tshirtsize = models.CharField(max_length=100)
    numcpus = models.CharField(max_length=100)
    operationalstatus = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    objects = QueryCMDBRecordsManager()

    class Meta:
        ordering = ('-name', '-date')

    def __str__(self):
        return self.hostname


# for sr create linux
class SRCreateServerLinuxRecordsManager(models.Manager):
    def create_SRCreateServerLinuxRecord(self, create_linux_sr_info):
        srcreateserverlinuxrecord = self.create(item=create_linux_sr_info['item'],
                                                operationusername=create_linux_sr_info['operationusername'],
                                                customer=create_linux_sr_info['customer'],
                                                customername=create_linux_sr_info['customername'],
                                                disasterlevelclass=create_linux_sr_info['disasterlevelclass'],
                                                hostname=create_linux_sr_info['hostname'],
                                                operationsystem=create_linux_sr_info['operationsystem'],
                                                environment=create_linux_sr_info['environment'],
                                                backup=create_linux_sr_info['backup'],
                                                servicelevel=create_linux_sr_info['servicelevel'],
                                                servicemodel=create_linux_sr_info['servicemodel'],
                                                retentionofbackup=create_linux_sr_info['retentionofbackup'],
                                                storegetier=create_linux_sr_info['storegetier'],
                                                serverbemanaged=create_linux_sr_info['serverbemanaged'],
                                                hypervisor=create_linux_sr_info['hypervisor'],
                                                securityzone=create_linux_sr_info['securityzone'],
                                                tshirtsize=create_linux_sr_info['tshirtsize'],
                                                vcpusize=create_linux_sr_info['vcpusize'],
                                                memsize=create_linux_sr_info['memsize'],
                                                srsubmitedinfo=create_linux_sr_info['srsubmitedinfo'])
        return srcreateserverlinuxrecord


class SRCreateServerLinuxRecord(models.Model):
    date = models.DateTimeField(auto_now=True, auto_created=True)
    operationusername = models.CharField(max_length=100, null=True)
    item = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    customername = models.CharField(max_length=100)
    disasterlevelclass = models.CharField(max_length=100)
    hostname = models.CharField(max_length=100)
    operationsystem = models.CharField(max_length=100)
    environment = models.CharField(max_length=100)
    backup = models.CharField(max_length=100)
    servicelevel = models.CharField(max_length=100)
    servicemodel = models.CharField(max_length=100)
    retentionofbackup = models.CharField(max_length=100)
    storegetier = models.CharField(max_length=100)
    serverbemanaged = models.CharField(max_length=100)
    hypervisor = models.CharField(max_length=100)
    securityzone = models.CharField(max_length=100)
    tshirtsize = models.CharField(max_length=100)
    vcpusize = models.CharField(max_length=100)
    memsize = models.CharField(max_length=100)
    srsubmitedinfo = models.CharField(max_length=300)

    objects = SRCreateServerLinuxRecordsManager()

    class Meta:
        ordering = ('-date',)

    def __str__(self):
        return self.hostname + ' - ' + self.srsubmitedinfo
