from django.shortcuts import render
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from reports.models import SaleReport, SaleOrder

def dashboard(request):
    yesterday = datetime.now() - timedelta(days=1)
    r_yesterday = SaleReport.objects.filter(type=1, date__day=yesterday.day, date__month=yesterday.month).order_by("-date").first()
    r_today = SaleReport.objects.filter(type=1).order_by("-date").first()
    r_week = SaleReport.objects.filter(type=1).order_by("-date")[:7]
    r_month = SaleReport.objects.filter(type=1).order_by("-date")[:30]
    t_yesterday = r_yesterday.total_income if r_yesterday else 0
    t_today = r_today.total_income
    t_week = sum(report.total_income for report in r_week)
    t_month = sum(report.total_income for report in r_month)
    reports = SaleReport.objects.filter(type=1)
    orders = SaleOrder.objects.filter(status=2)[:10]
    return render(request, "dashboard.html", {
        "t_yesterday": t_yesterday,
        "t_today": t_today,
        "t_week": t_week,
        "t_month": t_month,
        "reports": reports,
        "orders": orders
    })
