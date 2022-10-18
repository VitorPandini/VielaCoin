from pickle import FALSE
from django.shortcuts import redirect, render
from django.http import HttpResponse
from flask import jsonify
from posApp.models import Category, Products, Sales, salesItems, Employees
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse
import json, sys
from datetime import date, datetime

# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Usuário ou senha incorretos"
        else:
            resp['msg'] = "Usuário ou senha incorretos"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total',flat=True))
    context = {
        'page_title':'Home',
        'categories' : categories,
        'products' : products,
        'transaction' : transaction,
        'total_sales' : total_sales,
    }
    return render(request, 'posApp/home.html',context)


def about(request):
    context = {
        'page_title':'About',
    }
    return render(request, 'posApp/about.html',context)

#Employees
@login_required
def employees(request):
    employees_list = Employees.objects.all()
    # employees_list = {}
    context = {
        'page_title':'Employees List',
        'employees':employees_list,
    }
    return render(request, 'posApp/employees.html',context)

@login_required
def manage_employees(request):
    employee = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            employee = Employees.objects.filter(id=id).first()

    context = {
        'employee' : employee
    }
    return render(request, 'posApp/manage_employees.html',context)

@login_required
def save_employees(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_employees = Employees.objects.filter(id = data['code']).update(firstname=data['firstname'], lastname=data['lastname'], email = data['email'], saldo = float(data['saldo']), status = data['status'])
        else:
            save_employees = Employees(firstname=data['firstname'], lastname=data['lastname'], email = data['email'],saldo = float(data['saldo']), status = data['status'])
            save_employees.save()
        resp['status'] = 'success'
        messages.success(request, 'Empregado cadastrado com sucesso.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_emoloyees(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Employees.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Empregado excluído com sucesso.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")


#Categories
@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
    }
    return render(request, 'posApp/category.html',context)
@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()

    context = {
        'category' : category
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Categoria inserida com sucesso.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Categoria excluída com sucesso.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)
@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()

    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'posApp/manage_product.html',context)
def test(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'posApp/test.html',context)
@login_required
def save_product(request):
    data =  request.POST
    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Código do produto já cadastrado no banco de dados"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], description = data['description'], price = float(data['price']),status = data['status'])
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Produto incluído com sucesso.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Produto excluído com sucesso')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")
@login_required
def pos(request):

    employees = Employees.objects.filter(status = 1)
    employee_json = []

    products = Products.objects.filter(status = 1)
    product_json = []

    for employee in employees:
        employee_json.append({'id':employee.id, 'firstname':employee.firstname, 'lastname':employee.lastname, 'email':employee.email,'saldo':float(employee.saldo)})

    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price)})
    context = {
        'employees' : employees,
        'page_title' : "Point of Sale",
        'products' : products,
        'product_json' : json.dumps(product_json)
    }

    # return HttpResponse('')
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):



    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']
    context = {

        'grand_total' : grand_total,

    }
    return render(request, 'posApp/checkout.html',context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(code=code, sub_total = data['sub_total'], grand_total = data['grand_total'], tendered_amount = data['tendered_amount'], amount_change = data['amount_change']).save()
        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i]
            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty, 'price' : price, 'total' : total})
            salesItems(sale_id = sale, product_id = product, qty = qty, price = price, total = total).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Venda registrada com sucesso.")
    except:
        resp['msg'] = "Ocorreu um erro"
        -- print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def salesList(request):
    sales = Sales.objects.all()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html',context)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'posApp/receipt.html',context)
    # return HttpResponse('')

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'O registro de venda foi excluído.')
    except:
        resp['msg'] = "Ocorreu um erro"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')
