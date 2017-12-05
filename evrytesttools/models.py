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