from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.forms import inlineformset_factory ## multiple forms in forms
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm # django default form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required # restricted user access
from .decorators import unauthenticated_user, allowed_users, admin_only # custom restricted and allowed user acces
from django.contrib.auth.models import Group # Django signal to associated user with group

# Create your views here.
@login_required(login_url='login')
@admin_only # if customer the redirect to user-page and if admin redirect to view_func
def home(request):
    last_five_orders = Order.objects.all().order_by('-date_created')[:5]
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'last_five_orders':last_five_orders,
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required(login_url='login')
@admin_only # if customer the redirect to user-page and if admin redirect to view_func
def allOrders(request):
    orders = Order.objects.all()
    context = {
        'orders':orders,
    }

    return render(request, 'accounts/all_orders.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def customer(request, pk):
    customer = Customer.objects.get(id=pk)

    orders = customer.order_set.all()  # order_set means customers child order from model fields
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {
        'customer':customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter':myFilter
    }

    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=3) # Parent model and Child model. extra=3 means you will see three times form to place order 3 items together. You can use extra=10 or extra=5 as you wish.
    customer = Customer.objects.get(id=pk)

    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    # form = OrderForm(initial={'customer':customer}) # To see the customer in form, for which customer profile i viewd.

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('home')

    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) # to get pre-field form

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Update (instance) and Post
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/update_order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin']) # we can add more like - ['admin', 'staff', etc]
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()  # Now UserCreationForm will replace by CreateUserForm

    if request.method == 'POST':
        form = CreateUserForm(request.POST)  # Now UserCreationForm will replace by CreateUserForm
        if form.is_valid():
            user = form.save() # to associated user with group
            username = form.cleaned_data.get('username') # to associated user with group
            messages.success(request, 'Account was create for ' + username) # to associated user with group
            return redirect('login')

    context = {'form':form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password) # to check the user is in model/db or not.
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is Incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)

    return redirect('login')


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer # logged in user
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'accounts/account_settings.html', context)
