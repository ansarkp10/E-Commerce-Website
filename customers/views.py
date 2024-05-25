from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from . models import Customer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def sign_out(request):
    logout(request)
    return redirect('home')

def show_account(request):
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
                profile_picture = request.FILES.get('profile_picture')
                
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
                    name=username,
                    phone=phone,
                    address=address,
                    profile_picture=profile_picture  # Save profile picture to Customer model
                )
                return redirect('home')
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
                return redirect('home')
            else:
                messages.error(request, 'Invalid user credentials')
    
    return render(request, 'account.html', context)


def login_view(request):
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
                return redirect('home')
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
                return redirect('home')
            else:
                messages.error(request, 'Invalid user credentials')
    
    return render(request, 'account.html', context)

@login_required
def user_profile(request):
    try:
        user_profile = request.user.customer_profile
    except Customer.DoesNotExist:
        # If the user does not have a customer profile, create one
        customer = Customer.objects.create(user=request.user, name=request.user.username)
        user_profile = customer

    if request.method == 'POST':
        # Handle form submission
        user_profile.name = request.POST.get('name')
        user_profile.phone = request.POST.get('phone')
        user_profile.address = request.POST.get('address')
        user_profile.email = request.POST.get('email')
        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('my_profile')

    context = {'user_profile': user_profile, 'editable': True}  # Pass editable flag to template
    return render(request, 'user_profile.html', context)
