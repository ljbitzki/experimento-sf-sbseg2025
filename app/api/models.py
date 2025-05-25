from django.db import models

class Sot(models.Model):
    name = models.CharField(max_length=30, default="netbox-lab", unique=True)
    type = models.CharField(max_length=30, default="netbox")
    hostname = models.CharField(max_length=80, default="172.18.0.5")
    port = models.IntegerField(default=8080)
    token = models.CharField(max_length=120, default="0123456789abcdef0123456789abcdef01234567")

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

