from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm
from django.forms import inlineformset_factory ## multiple forms in forms
from .filters import OrderFilter

# Create your views here.
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()

    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {
        'orders':orders,
        'customers':customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending
    }

    return render(request, 'accounts/dashboard.html', context)

def products(request):
    products = Product.objects.all()

    return render(request, 'accounts/products.html', {'products':products})

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


def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10) # Parent model and Child model
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


def updateOrder(request, pk):
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order) # to get pre-field form

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order) # Update (instance) and Post
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)


def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('home')

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)
