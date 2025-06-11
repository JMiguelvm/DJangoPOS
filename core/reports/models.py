from django.db import models
from django.utils import timezone
from products.models import Product
from customers.models import Customer
from datetime import timedelta, time
import calendar

class SaleReport(models.Model):
    options = [
        (1, "Diario"),
        (2, "Semanal"),
        (3, "Mensual")
    ]
    type = models.IntegerField(choices=options, default=None, null=True)
    date = models.DateTimeField(null=True) # Siempre date pertenece a el primer día
    total_income = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    net_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    def __str__(self):
        return f"ID:{self.id} /-/ {self.total_income} /-/ {self.options[self.type - 1]}"
    
class SaleOrder(models.Model):
    options = [
        (1, "Borrador"),
        (2, "Publicada"),
        (3, "Anulada")
    ]
    date = models.DateTimeField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, default=None)
    status = models.IntegerField(choices=options, default=1)
    def __str__(self):
        return f"ID:{self.id}  /-/ {self.options[self.status-1][1]}"

class OrderItem(models.Model):
    order = models.ForeignKey(SaleOrder, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    iva = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField()
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # Extends post-save in order item
    def save(self, *args, **kwargs):

        is_update = self.pk is not None
        old_item = None
        if is_update:
            try:
                old_item = OrderItem.objects.get(pk=self.pk)
            except OrderItem.DoesNotExist:
                old_item = None

        if self.product:
            self.iva = self.product.iva
        # Call original save method
        super().save(*args, **kwargs)
        if self.order.status == 2:
            now = timezone.now()
            old_sell_total = old_item.sell_price * old_item.quantity if old_item else 0
            old_buy_total = old_item.buy_price * old_item.quantity if old_item else 0
            total_sell_price = self.sell_price * self.quantity - old_sell_total
            total_buy_price = self.buy_price * self.quantity - old_buy_total

            # --------- REPORT DAY --------------
            # Check if had report in that day
            start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
            report_day = SaleReport.objects.filter(
            date__range=(start_of_day, end_of_day),
            type=1
            ).first() # Get just one
            # If exist a report day
            if report_day:
                report_day.total_income += total_sell_price
                report_day.net_profit += total_sell_price - total_buy_price
            else:
                report_day = SaleReport.objects.create(
                    date=start_of_day,
                    type=1
                )
                report_day.total_income += total_sell_price
                report_day.net_profit += total_sell_price - total_buy_price
            report_day.save()
            
            # --------- REPORT WEEK --------------
            # Check if had report in that week
            start_of_week = start_of_day.replace(day=start_of_day.day - start_of_day.weekday())
            end_of_week = end_of_day + timedelta(days=(6 - start_of_week.weekday()))
            report_week = SaleReport.objects.filter(
            date__range=(start_of_week, end_of_week),
            type=2
            ).first()
            if report_week:
                report_week.total_income += total_sell_price
                report_week.net_profit += total_sell_price - total_buy_price
            else:
                report_week = SaleReport.objects.create(
                    date=start_of_week,
                    type=2
                )
                report_week.total_income += total_sell_price
                report_week.net_profit += total_sell_price - total_buy_price
            report_week.save()

            # --------- REPORT MONTH --------------
            # Check if had report in that month
            start_of_month = start_of_day.replace(day=1)
            end_of_month = end_of_day.replace(day=(calendar.monthrange(end_of_day.year, end_of_day.month))[1])
            report_month = SaleReport.objects.filter(
            date__range=(start_of_month, end_of_month),
            type=3
            ).first()
            if report_month:
                report_month.total_income += total_sell_price
                report_month.net_profit += total_sell_price - total_buy_price
            else:
                report_month = SaleReport.objects.create(
                    date=start_of_month,
                    type=3
                )
                report_month.total_income += total_sell_price
                report_month.net_profit += total_sell_price - total_buy_price
            report_month.save()
