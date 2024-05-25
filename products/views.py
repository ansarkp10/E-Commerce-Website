from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Product
from customers.models import Customer
from orders.models import Order,OrderItem
from django.db.models import Q  # Add this import statement
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField, Sum
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages


def index(request):
    return render(request, 'index.html')

def list_products(request):
    page = request.GET.get('page', 1)
    product_list = Product.objects.filter(delete_status=Product.LIVE).order_by('priority')
    paginator = Paginator(product_list, 3)
    products = paginator.get_page(page)
    return render(request, 'products.html', {'products': products})

def detail_product(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def search_products(request):
    query = request.GET.get('q')
    if query:
        product_list = Product.objects.filter(
            (Q(title__icontains=query) | Q(description__icontains=query)) &
            Q(delete_status=Product.LIVE)
        ).order_by('priority')
    else:
        product_list = Product.objects.none()  # Empty queryset if no search query
    paginator = Paginator(product_list, 3)
    page = request.GET.get('page', 1)
    products = paginator.get_page(page)
    return render(request, 'search_results.html', {'products': products, 'query': query})

@login_required
def order_to_cart(request,pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

def orderlogin(request):
    context = {}
    if request.method == 'POST':
        if 'register' in request.POST:
            context['register'] = True
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                email = request.POST.get('email')
                address = request.POST.get('address')
                phone = request.POST.get('phone')
                
                # Check if the user already exists
                if User.objects.filter(username=username).exists():
                    raise Exception("Username already exists")
                
                # Create user account
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=email
                )
                # Create customer account
                customer = Customer.objects.create(
                    user=user,
                    name=username,  # Assuming name is same as username
                    phone=phone,
                    address=address
                )
                return redirect('list_product')
            except Exception as e:
                error_message = str(e)
                messages.error(request, error_message)

        elif 'login' in request.POST:
            context['register'] = False
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('list_product')
            else:
                messages.error(request, 'Invalid user credentials')
    
    return render(request, 'account.html', context)