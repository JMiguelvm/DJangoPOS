from django.shortcuts import render
from datetime import timedelta
from django.utils import timezone
from reports.models import SaleReport, SaleOrder
from django.db.models import Sum, F

def dashboard(request):
    now = timezone.localtime(timezone.now())
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
    yesterday_start = today_start - timedelta(days=1)
    yesterday_end = today_start - timedelta(seconds=1)

    # Reporte de ayer (rango de todo el día de ayer)
    r_yesterday = SaleReport.objects.filter(
        type=1,
        date__range=(yesterday_start, yesterday_end)
    ).order_by("-date").first()

    # Reporte de hoy (rango de todo el día de hoy)
    r_today = SaleReport.objects.filter(
        type=1,
        date__range=(today_start, today_end)
    ).order_by("-date").first()

    # Últimos 7 y 30 días (incluyendo hoy)
    r_week = SaleReport.objects.filter(
        type=1,
        date__gte=today_start - timedelta(days=6),
        date__lte=today_end
    ).order_by("-date")
    r_month = SaleReport.objects.filter(
        type=1,
        date__gte=today_start - timedelta(days=29),
        date__lte=today_end
    ).order_by("-date")

    t_yesterday = r_yesterday.total_income if r_yesterday else 0
    t_today = r_today.total_income if r_today else 0
    t_week = sum(report.total_income for report in r_week)
    t_month = sum(report.total_income for report in r_month)

    reports = SaleReport.objects.filter(
        type=1,
        date__gte=today_start - timedelta(days=29),
        date__lte=today_end
    ).order_by("-date")

    orders = SaleOrder.objects.filter(status=2).annotate(
        total_sell_value=Sum(F('orderitem__quantity') * F('orderitem__sell_price'))
    ).order_by("-date")[:10]

    return render(request, "dashboard.html", {
        "t_yesterday": t_yesterday,
        "t_today": t_today,
        "t_week": t_week,
        "t_month": t_month,
        "reports": reports,
        "orders": orders
    })

def error_404(request, exception):
    return render(request, 'error/404.html', status=404)

def error_500(request):
    return render(request, 'error/500.html', status=500)