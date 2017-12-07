from django.db import models


# Create your models here.

class VIOinfo(models.Model):
    instancename = models.CharField(max_length=100)
    imagename = models.CharField(max_length=100)
    ip = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    availabilityzone = models.CharField(max_length=100)
    powerstate = models.CharField(max_length=100)

    class Meta:
        ordering = ('-instancename',)

    def __str__(self):
        return self.instancename


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
