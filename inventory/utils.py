from django.shortcuts import render, redirect
from django.db.models.functions import Lower
from django.db.models import Sum, F
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from datetime import timedelta, time
from dateutil.relativedelta import relativedelta
from calendar import monthrange
from django.db.models.functions import TruncMonth, TruncWeek
import random
from .models import Product, Vendor, Category, Customer, Debt, OrderItem, SaleOrder, ProductStock, SaleReport


def _report_by_date(start, end, report_type):
    orders_today = SaleOrder.objects.filter(
        date__range=(start, end),
        status=2,
        registered = False
    )

    total_amount = OrderItem.objects.filter(
        order__in=orders_today
    ).aggregate(
        total=Sum(F('quantity') * (F('price')-F('buy_price')))
    )['total'] or 0
    
    report, created = SaleReport.objects.update_or_create(
        date__range=(start, end),
        type=report_type,
        defaults={'amount': total_amount, 'date': start}
    )
    for order in orders_today:
        if report_type == 1:
            order.registered = True
            order.save()
    return report

def calculate_day():
    now = timezone.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    _report_by_date(start_of_day, end_of_day, 1)
# Recibe la instancia de tiempo, y va al primer día, de la respectiva instancia de tiempo
# Por ejemplo, si recibe un jueves, el primer día será un lunes y el ultimo un domingo a las 23:59
def calculate_week(time_instance):
    start_of_week = time_instance - timedelta(days=time_instance.weekday())
    if start_of_week.month != time_instance.month:
        start_of_week = time_instance.replace(day=1)
    end_of_week = start_of_week + timedelta(days=(6 - start_of_week.weekday()))
    if start_of_week.month != end_of_week.month:
        end_of_week = monthrange(start_of_week.year, start_of_week.month)[1]
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=1)
    end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)
    total_amount = SaleReport.objects.filter(
    date__range=(start_of_week, end_of_week),
    type=1
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    a = []
    a.append(f'{start_of_week} ------- {end_of_week} ----- {total_amount}')
    SaleReport.objects.create(type=2, amount=total_amount, date=start_of_week)
    return a

    

# Recibe la instancia de tiempo, y va al primer día del mes, de la respectiva instancia de tiempo
# Por ejemplo, si recibe un jueves 15, el primer día será un lunes 1 y el ultimo un domingo 30/31 a las 23:59 (O lo correspondiente de ese mes) 
def calculate_month(time_instance):
    time_instance.replace(hour=12, minute=00, second=0, microsecond=1)
    start_of_month = time_instance.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    last_day = monthrange(time_instance.year, time_instance.month)[1]
    end_of_month = time_instance.replace(day=last_day, hour=23, minute=59, second=59, microsecond=999999)
    total_amount = SaleReport.objects.filter(
    date__range=(start_of_month, end_of_month),
    type=2
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    SaleReport.objects.create(type=3, amount=total_amount, date=start_of_month)


def recalculate_days(start=None, end=None):
    """
    Nothing if you want to recalculate all.
    """
    if start and end:
        orders = SaleOrder.objects.filter(
            date__range=(start, end),
            status=2
        ).order_by('date')
    else:
        orders = SaleOrder.objects.filter(
            status=2
        ).order_by('date')
        if not orders:
            return []  # No orders to process

        start = orders.first().date

    current_day = start.date()
    current_time = start
    last_day = (orders.last().date + timedelta(days=1)).date()
    a = []

    while current_day < last_day:
        total_amount = 0
        s_day = current_time.replace(hour=0, minute=0, second=0, microsecond=1)
        e_day = current_time.replace(hour=23, minute=59, second=59, microsecond=999999)
        c_orders = orders.filter(date__range=(s_day, e_day))

        total_amount = sum(
            OrderItem.objects.filter(order=c_order).aggregate(
                total=Sum(F('quantity') * (F('price') - F('buy_price')))
            )['total'] or 0
            for c_order in c_orders
        )

        if total_amount:
            report, created = SaleReport.objects.update_or_create(
                date=s_day,
                type=1,
                defaults={'amount': total_amount}
            )
            a.append('Reporte creado' if created else 'Reporte actualizado')

        a.append(f'{s_day} -------- {e_day} ---- c time {current_time}--- time {current_time} --- total === {total_amount}')
        current_day += timedelta(days=1)
        current_time += timedelta(days=1)
    
    orders.update(registered=True)
    return a

def recalculate_weeks(start=None, end=None):
    """
    Nothing if you want to recalculate all.
    """
    if start and end:
        reports = SaleReport.objects.filter(
            date__range=(start, end),
            type=1
        ).order_by('date')
    else:
        reports = SaleReport.objects.filter(
            type=1
        ).order_by('date')
        if not reports:
            return []  # No orders to process

        start = reports.first().date

    current_day = start.date()
    current_time = start
    last_day = (reports.last().date + timedelta(days=1)).date()
    a = []

    while current_day < last_day:
        total_amount  = 0
        start_of_week = current_time - timedelta(days=current_time.weekday())
        if start_of_week.month != current_time.month:
            start_of_week = current_time.replace(day=1)
        end_of_week = start_of_week + timedelta(days=(6 - start_of_week.weekday()))
        if start_of_week.month != end_of_week.month:
            end_of_week = start_of_week.replace(day=monthrange(start_of_week.year, start_of_week.month)[1])
        start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=1)
        end_of_week = end_of_week.replace(hour=23, minute=59, second=59, microsecond=999999)

        total_amount = (
            SaleReport.objects.filter(
                type=1,
                date__range=(start_of_week, end_of_week)
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )
        if total_amount:
            report, created = SaleReport.objects.update_or_create(
                date=start_of_week,
                type=2,
                defaults={'amount': total_amount}
            )
            a.append('Reporte creado' if created else 'Reporte actualizado')

        a.append(f'{start_of_week} -------- {end_of_week} ---- c time {current_time}--- time {current_time} --- total === {total_amount}')
        current_day += timedelta(days=7)
        current_time += timedelta(days=7)
    return a

def recalculate_months(start=None, end=None):
    """
    Nothing if you want to recalculate all.
    """
    if start and end:
        reports = SaleReport.objects.filter(
            date__range=(start, end),
            type=2
        ).order_by('date')
    else:
        reports = SaleReport.objects.filter(
            type=2
        ).order_by('date')
        if not reports:
            return []  # No orders to process

        start = reports.first().date

    current_day = start.date()
    current_time = start
    last_day = (reports.last().date + timedelta(days=1)).date()
    a = []

    while current_day < last_day:
        total_amount  = 0
        start_of_month = current_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_month = monthrange(current_time.year, current_time.month)[1]
        end_of_month = current_time.replace(day=last_day_month, hour=23, minute=59, second=59, microsecond=999999)

        total_amount = (
            SaleReport.objects.filter(
                type=2,
                date__range=(start_of_month, end_of_month)
            ).aggregate(
                total=Sum('amount')
            )['total'] or 0
        )
        if total_amount:
            report, created = SaleReport.objects.update_or_create(
                date=start_of_month,
                type=3,
                defaults={'amount': total_amount}
            )
            a.append('Reporte creado' if created else 'Reporte actualizado')

        a.append(f'{start_of_month} -------- {end_of_month} ---- c time {current_time}--- time {current_time} --- total === {total_amount}')
        current_day += relativedelta(months=1)
        current_time += relativedelta(months=1)
    return a