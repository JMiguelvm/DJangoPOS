from django.db import models
from django.utils import timezone

class Customer(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Debt(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField()
    date = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f"{self.customer} — {self.amount}"