from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, default=None)

    def __str__(self):
        return self.name