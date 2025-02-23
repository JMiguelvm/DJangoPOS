from django.db import models

class Vendor(models.Model):
    name = models.CharField(max_length=128)
    numberPhone = models.IntegerField(null=True, default=None)
    description = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name