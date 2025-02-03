from django.shortcuts import render, redirect
from django.db.models.functions import Lower
from django.db.models import Sum, F
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from faker import Faker
from datetime import timedelta, time
import faker_commerce
import random
import json
import calendar
from .utils import recalculate_days, recalculate_weeks, recalculate_months, calculate_month, calculate_week
from .models import Product, Vendor, Category, Customer, Debt, OrderItem, SaleOrder, ProductStock, SaleReport

# Create your views here.
def dashboard(request):
    today = timezone.now()
    if calendar.monthrange(today.year, today.month)[1] == 31:
        start = today - timedelta(days=31)
    else:
        start = today - timedelta(days=30)
    recalculate_days(start, today)
    reports = SaleReport.objects.filter(
        date__range=(start, today),
        type=1
    ).order_by('date')

    r_today  = SaleReport.objects.filter(
        date__range=(today.replace(hour=0, minute=0, second=0, microsecond=0), today.replace(hour=23, minute=59, second=59, microsecond=999999)),
        type=1
    ).first()
    r_yesterday  = SaleReport.objects.filter(
        date__range=(today.replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(days=1), today.replace(hour=23, minute=59, second=59, microsecond=999999)-timedelta(days=1)),
        type=1
    ).first()
    r_week = SaleReport.objects.filter(
        date__range=(today.replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(days=7), today.replace(hour=23, minute=59, second=59, microsecond=999999)),
        type=1
    )
    week_t_amount = 0
    for r in r_week:
        week_t_amount += r.amount

    r_month = SaleReport.objects.filter(
        date__range=(today.replace(hour=0, minute=0, second=0, microsecond=0)-timedelta(days=30), today.replace(hour=23, minute=59, second=59, microsecond=999999)),
        type=1
    )
    month_t_amount = 0
    for r in r_month:
        month_t_amount += r.amount
    orders_today = SaleOrder.objects.filter(
        date__range=(today.replace(hour=0, minute=0, second=0, microsecond=0), today.replace(hour=23, minute=59, second=59, microsecond=999999)),
        status=2,
        registered = True
    )

    total_amount = OrderItem.objects.filter(
        order__in=orders_today
    ).aggregate(
        total=Sum(F('quantity') * (F('price')-F('buy_price')))
    )['total'] or 0
    last_orders = SaleOrder.objects.all().order_by('-date')[:10]
    context = {
        'reports': reports,
        'r_today': "{:,.2f}".format(r_today.amount) if r_today else 0,
        'r_yesterday': "{:,.2f}".format(r_yesterday.amount) if r_yesterday else 0,
        'r_week': "{:,.2f}".format(week_t_amount),
        'r_month': "{:,.2f}".format(month_t_amount),
        'total_amount': total_amount,
        'last_orders': last_orders
        }
    return render(request, "dashboard.html", context)


def productList(request):
    if request.method == 'GET':
        productList = Product.objects.all()
    elif request.method == 'POST' and 'sort_alphabetically' in request.POST:
        productList = Product.objects.annotate(lower_name=Lower('name')).order_by('lower_name')
    pagination = Paginator(productList, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    vendors = Vendor.objects.all()
    categorys = Category.objects.all()
    return render(request, "productList.html", {'page_obj': pageObj, "vendors": vendors, "categorys": categorys})

def addProduct(request):
    name = request.POST['txtProductName']
    price = request.POST['numberProductPrice']
    vendor = Vendor.objects.get(id=request.POST['selectVendor'])
    category = Category.objects.get(id=request.POST['selectCategory'])
    if request.POST['textAreaProductDescription']:
        description = request.POST['textAreaProductDescription']
        product = [name, price, description, vendor, category]
    else:
        product = [name, price, '', vendor, category]
    if request.POST['bar_code']:
        bar_code = request.POST['bar_code']
    else:
        bar_code = 0
    product.append(bar_code)
    Product.objects.create(name=product[0], price=product[1], description=product[2], vendor=product[3], category=product[4], bar_code=product[5])
    return redirect('/product')

def editProduct(request):
    # View in entrance, with ID form product list
    if 'buttonId' in request.POST:
        buttonId = request.POST['buttonId']
        product = Product.objects.get(id=buttonId)
        productPriceInt = int(product.price)
        productSellPriceInt = int(product.sell_price)
        vendors = Vendor.objects.all()
        categorys = Category.objects.all()
        return render(request, "editProduct.html", {"product": product, "productPriceInt": productPriceInt, "vendors": vendors, "categorys": categorys, "productSellPriceInt": productSellPriceInt})
    # View when press 'save' button, manage db save changes.
    elif request.method == 'POST' and 'txtProductName' in request.POST:
        product = Product.objects.get(id=request.POST['productId'])
        product.name = request.POST['txtProductName']
        product.price = request.POST['numberProductPrice']
        category = Category.objects.get(id=request.POST['selectCategory'])
        product.category = category
        vendor = Vendor.objects.get(id=request.POST['selectVendor'])
        product.vendor = vendor
        if request.POST['bar_code']:
            product.bar_code = request.POST['bar_code']
        else:
            product.bar_code = 0
        if request.POST['textAreaProductDescription']:
            product.description = request.POST['textAreaProductDescription']
        product.save()
        return redirect('/product')

def deleteProduct(request):
    if 'productId' in request.POST:
        productId = request.POST['productId']
        product = Product.objects.get(id=productId)
        product.delete()
        return redirect('/product')
    else:
        return redirect('/product')

def searchProduct(request):
    inputSearch = request.POST['inputSearch']
    products = Product.objects.filter(name__istartswith = inputSearch)
    if products:
        searchResult = 1
    else:
        products = Product.objects.all()
        searchResult = 0
    pagination = Paginator(products, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "productList.html", {'page_obj': pageObj, "searchResult": searchResult})


# Vendor section

def vendorList(request):
    if request.method == 'GET':
        vendorList = Vendor.objects.all()
    elif request.method == 'POST' and 'sort_alphabetically' in request.POST:
        vendorList = Vendor.objects.annotate(lower_name=Lower('name')).order_by('lower_name')
    pagination = Paginator(vendorList, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "vendorList.html", {'page_obj': pageObj})

def addVendor(request):
    name = request.POST['txtVendorName']
    numberPhone = request.POST['numberVendorNumberPhone']
    if request.POST['textAreaVendorDescription']:
        description = request.POST['textAreaVendorDescription']
        vendor = [name, numberPhone, description]
    else:
        vendor = [name, numberPhone, '']
    Vendor.objects.create(name=vendor[0], numberPhone=vendor[1], description=vendor[2])
    return redirect('/vendor')

def editVendor(request):
    if 'buttonId' in request.POST:
        buttonId = request.POST['buttonId']
        vendor = Vendor.objects.get(id=buttonId)
        return render(request, "editVendor.html", {"vendor": vendor})
    elif request.method == 'POST' and 'txtVendorName' in request.POST:
        vendor = Vendor.objects.get(id=request.POST['vendorId'])
        vendor.name = request.POST['txtVendorName']
        vendor.numberPhone = request.POST['numberVendorNumberPhone']
        if request.POST['textAreaVendorDescription']:
            vendor.description = request.POST['textAreaVendorDescription']
        vendor.save()
        return redirect('/vendor')

def deleteVendor(request):
    if 'vendorId' in request.POST:
        vendorId = request.POST['vendorId']
        vendor = Vendor.objects.get(id=vendorId)
        vendor.delete()
        return redirect('/vendor')
    else:
        return redirect('/vendor')

def searchVendor(request):
    inputSearch = request.POST['inputSearch']
    vendor = Vendor.objects.filter(name__istartswith = inputSearch)
    if vendor:
        searchResult = 1
    else:
        vendor = Vendor.objects.all()
        searchResult = 0
    pagination = Paginator(vendor, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "vendorList.html", {'page_obj': pageObj, "searchResult": searchResult})

# Category section

def categoryList(request):
    if request.method == 'GET':
        categoryList = Category.objects.all()
    elif request.method == 'POST' and 'sort_alphabetically' in request.POST:
        categoryList = Category.objects.annotate(lower_name=Lower('name')).order_by('lower_name')
    pagination = Paginator(categoryList, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "categoryList.html", {'page_obj': pageObj})

def addCategory(request):
    name = request.POST['txtCategoryName']
    if request.POST['textAreaCategoryDescription']:
        description = request.POST['textAreaCategoryDescription']
        category = [name, description]
    else:
        category = [name, '']
    Category.objects.create(name=category[0], description=category[1])
    return redirect('/category')

def editCategory(request):
    if 'buttonId' in request.POST:
        buttonId = request.POST['buttonId']
        category = Category.objects.get(id=buttonId)
        return render(request, "editCategory.html", {"category": category})
    elif request.method == 'POST' and 'txtVendorName' in request.POST:
        category = Category.objects.get(id=request.POST['vendorId'])
        category.name = request.POST['txtVendorName']
        if request.POST['textAreaVendorDescription']:
            category.description = request.POST['textAreaVendorDescription']
        category.save()
        return redirect('/category')

def deleteCategory(request):
    if 'categoryId' in request.POST:
        categoryId = request.POST['categoryId']
        category = Category.objects.get(id=categoryId)
        category.delete()
        return redirect('/category')
    else:
        return redirect('/category')

def searchCategory(request):
    inputSearch = request.POST['inputSearch']
    category = Category.objects.filter(name__istartswith = inputSearch)
    if category:
        searchResult = 1
    else:
        category = Category.objects.all()
        searchResult = 0
    pagination = Paginator(category, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "categoryList.html", {'page_obj': pageObj, "searchResult": searchResult})

# Customer section

def customerList(request):
    if request.method == 'GET':
        customerList = Customer.objects.all()
    elif request.method == 'POST' and 'sort_alphabetically' in request.POST:
        customerList = Customer.objects.annotate(lower_name=Lower('name')).order_by('lower_name')
    
    for customer in customerList:
        debts = Debt.objects.filter(customer = customer.id)
        totalAmount = 0
        for debt in debts:
            totalAmount += debt.amount
        customer.total_amount = totalAmount
    pagination = Paginator(customerList, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
        
    return render(request, "customerList.html", {'page_obj': pageObj})

def addCustomer(request):
    name = request.POST['txtCustomerName']
    category = [name]
    Customer.objects.create(name=category[0])
    return redirect('/customer')

def editCustomer(request):
    if 'buttonId' in request.POST and 'inputName' in request.POST:
        buttonId = request.POST['buttonId']
        customer = Customer.objects.get(id=buttonId)
        customer.name = request.POST['inputName']
        customer.save()
        return redirect('/customer')

def deleteCustomer(request):
    if 'categoryId' in request.POST:
        categoryId = request.POST['categoryId']
        category = Customer.objects.get(id=categoryId)
        category.delete()
        return redirect('/category')
    else:
        return redirect('/category')

def searchCustomer(request):
    inputSearch = request.POST['inputSearch']
    customer = Customer.objects.filter(name__istartswith = inputSearch)
    if customer:
        searchResult = 1
    else:
        customer = Customer.objects.all()
        searchResult = 0
    pagination = Paginator(customer, 10)
    pageNumber = request.GET.get('page')
    pageObj = pagination.get_page(pageNumber)
    return render(request, "customerList.html", {'page_obj': pageObj, "searchResult": searchResult})

# Debt section
def debtView(request):
    customerId = request.POST['customerId']
    customer = Customer.objects.get(id = customerId)
    debts = Debt.objects.filter(customer = customer)
    totalAmount = 0
    for debt in debts:
        totalAmount += debt.amount
    return render(request, "debtView.html", {'customer': customer, "debts": debts, "totalAmount": totalAmount})

def addDebt(request):
    imputDate = request.POST['debtDate']
    imputAmount = request.POST['debtAmount']
    imputCustomerId = request.POST['debtCustomer']
    customerInstance = Customer.objects.get(id = imputCustomerId)
    Debt.objects.create(customer=customerInstance, amount=imputAmount, date=imputDate)
    return redirect('/customer')

def deleteDebt(request):
    if 'debtId' in request.POST:
        debtId = request.POST['debtId']
        debt = Debt.objects.get(id=debtId)
        debt.delete()
        return redirect('/customer')
    else:
        return redirect('/customer')
    
# POS Section

def posView(request):
    if 'nInputs' in request.POST:
        nInputs = request.POST['nInputs']
        if 'draft' in request.POST:
            new_order = SaleOrder.objects.create(status=1)
        elif 'publish' in request.POST:
            if 'customer' in request.POST:
                actual_customer = Customer.objects.get(id=request.POST['customer'])
                actual_debt = int(request.POST['debt'])*-1
                Debt.objects.create(customer=actual_customer, amount=actual_debt)
                new_order = SaleOrder.objects.create(status=2, customer=actual_customer)
            else:
                new_order = SaleOrder.objects.create(status=2)
        c_order = new_order.id
        if 'delete' in request.POST:
            d_id = request.POST['delete']
            d_order = SaleOrder.objects.get(id=d_id)
            d_order.delete()
        for i in range(int(nInputs)):
            str_p = f"p{i}"
            str_q = f"q{i}"
            quantity = request.POST[str_q]
            product_id = request.POST[str_p]
            i_product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=new_order, product=i_product, quantity=quantity, price=i_product.price)
    else:
        c_order = False
    products = Product.objects.all()
    customer = Customer.objects.all()
    categorys = Category.objects.all()
    orders = SaleOrder.objects.order_by('-date')
    for actual_order in orders:
        actual_items = OrderItem.objects.filter(order=actual_order)
        actual_order.total = 0
        for item in actual_items:
            actual_order.total += item.price * item.quantity
    if request.GET.get('order'):
        order_id = request.GET.get('order')
        order = SaleOrder.objects.get(id=order_id)
        if order.status == 1:
            order_items = OrderItem.objects.filter(order=order)
            total = 0
            if order_items:
                for item in order_items:
                    actual_price = item.price * item.quantity
                    total += actual_price
                for item in order_items:
                    item.total_price = item.price * item.quantity
        else:
            order = []
            order_items = []
    else:
        order = []
        order_items = []
    pagination = Paginator(orders, 10)
    pageNumber = request.GET.get('page')
    order_pages = pagination.get_page(pageNumber)
    if not pageNumber:
        page = False
    else:
        page = True
    # Products with bar_code
    product_bc = {}
    test = []
    for product in products:
        if product.bar_code != "0":
            product_bc[f"{product.bar_code}"] = {
            "id": product.pk,
            "name": product.name,
            "price": product.price
        }
    p_w_bar_code = json.dumps(product_bc)
    return render(request, "posView.html", {
        "products": products,
         "categorys": categorys,
         "customer": customer,
         "order": order,
         "order_items": order_items,
         "order_pages": order_pages,
         "page": page,
         "c_order": c_order,
         "bc_products": p_w_bar_code
         })

def orderView(request):
    if request.method == 'GET' and request.GET.get('order'):
        order_id = request.GET.get('order')
        order = SaleOrder.objects.get(id=order_id)
        order_items = OrderItem.objects.filter(order=order)
        total = 0
        if order_items:
            for item in order_items:
                actual_price = item.price * item.quantity
                total += actual_price
            for item in order_items:
                item.total_price = item.price * item.quantity
        return render(request, "orderView.html", {"order": order, "order_items": order_items, "total": total})
    else:
        return redirect('/pos')
    

def productStockList(request):
    if request.method == 'GET':
        productStockList = Product.objects.all()
    elif request.method == 'POST' and 'sort_alphabetically' in request.POST:
        productStockList = Product.objects.annotate(lower_name=Lower('name')).order_by('lower_name')

    search_query = request.POST.get('inputSearch', '')
    if search_query:
        productStockList = Product.objects.filter(name__icontains=search_query)

    products = Product.objects.all()
    vendors = Vendor.objects.all()

    pagination = Paginator(productStockList, 10)
    page_number = request.GET.get('page')
    page_obj = pagination.get_page(page_number)

    return render(request, "stockList.html", {
        'page_obj': page_obj, 
        'searchResult': productStockList.count(),
        'products': products,
        'vendors': vendors
        })

def addStock(request):
    return render(request, "stockList.html", {
        })
def productStock(request):
    product = Product.objects.get(id=request.GET.get('product'))
    stock = ProductStock.objects.filter(product=product).order_by('-date')
    return render(request, "stockView.html", {
        'product': product,
        'stock': stock
        })

    
def createData(request):
    # f_products = []
    # f_vendors = []
    # f_category = []
    # f_order = []
    # f_item_order = []
    # fake = Faker()
    # fake.add_provider(faker_commerce.Provider)
    # for _ in range(1):
    #     vendor = Vendor.objects.create(name=fake.company(), numberPhone=fake.numerify('######'), description=fake.text())
    #     f_vendors.append(vendor)
    # for _ in range(1):
    #     category = Category.objects.create(name=fake.ecommerce_category(), description=fake.text())
    #     f_category.append(category)
    # for _ in range(3):
    #     product = Product.objects.create(name=fake.ecommerce_name(), price=fake.numerify('######'), category=random.choice(f_category), vendor=random.choice(f_vendors))
    #     f_products.append(product)
    # for _ in range(40):
    #     order = SaleOrder.objects.create(status=2, date=fake.date_between(timezone.now()-timedelta(days=30)))
    #     f_order.append(order)
    # for order in f_order:
    #     item = []
    #     for _ in range(5):
    #         product = random.choice(f_products)
    #         item_order = OrderItem.objects.create(order=order, product=product, price=product.price, quantity=random.randint(1, 8))
    #         item.append(item_order)
    #     f_item_order.append(item)
    recalculate_days()
    recalculate_weeks()
    a = recalculate_months()
    
    return render(request, 'test.html', {'a':a})