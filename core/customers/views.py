from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Customer, Debt
from datetime import datetime

def index(request):
    customers = Customer.objects.all()
    for customer in customers:
        debts = Debt.objects.filter(customer=customer)
        customer.t_debt = 0
        for debt in debts:
            customer.t_debt += debt.amount
    return render(request, "customers/index.html", {"customers": customers})

def edit(request):
    # Edit customer
    if request.method == "POST" and request.POST.get('name'):
        name = request.POST.get('name')
        customer = Customer.objects.get(id=request.POST.get('id'))
        customer.name = name
        customer.save()
        return redirect('customers:index')
    # Delete customer
    elif request.method == "GET" and request.GET.get('delete'):
        customer = Customer.objects.get(id=request.GET.get('delete'))
        customer.delete()
        return redirect('customers:index')
    # Delete debt
    elif request.method == "GET" and request.GET.get('delete_debt'):
        debt = Debt.objects.get(id=request.GET.get('delete_debt'))
        debt.delete()
        return redirect('customers:index')
    customer = Customer.objects.get(id=request.GET.get('id'))
    debts = Debt.objects.filter(customer=customer)
    # Calculate total debt
    t_debt = 0
    for debt in debts:
        t_debt += debt.amount
    return render(request, "customers/edit.html", {"customer": customer, "debts": debts, "t_debt": t_debt})

def create(request):
    # Create customer
    if request.method == "POST" and request.POST.get('name'):
        name = request.POST['name']
        Customer.objects.create(name=name)
        return redirect('customers:index')
    # Create debt customer
    elif request.method == "POST" and request.POST.get('id'):
        datetime_str = request.POST.get('datetime')
        if datetime_str:
            try:
                dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
            except ValueError:
                dt = datetime.now()
        customer = Customer.objects.get(id=request.POST['id'])
        amount = request.POST['amount']
        Debt.objects.create(customer=customer, amount=amount, date=dt)
        return redirect(reverse('customers:edit') + f'?id={customer.id}')
    return render(request, "customers/create.html")