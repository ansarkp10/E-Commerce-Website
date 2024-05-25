from django.shortcuts import render, redirect, HttpResponse
from .models import Order, OrderItem
from products.models import Product
from customers.models import Customer
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseServerError
from decimal import Decimal
from django.db.models import F, ExpressionWrapper, DecimalField, Sum

def show_cart(request):
    user = request.user
    customer = user.customer_profile
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_SATGE
    )
    # Calculate subtotal
    subtotal_expr = ExpressionWrapper(F('product__price') * F('quantity'), output_field=DecimalField())
    subtotal = cart_obj.added_item.annotate(subtotal=subtotal_expr).aggregate(subtotal_sum=Sum('subtotal'))['subtotal_sum'] or Decimal('0')

    # Calculate tax (assuming it's 10%)
    tax_rate = Decimal('0.10')
    tax = subtotal * tax_rate

    # Calculate total
    total = subtotal + tax

    context = {'cart': cart_obj, 'subtotal': subtotal, 'tax': tax, 'total': total}
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            return HttpResponseServerError("Customer profile does not exist")
        
        quantity = int(request.POST.get('quantity'))
        product_id = request.POST.get('product_id')
        
        try:
            cart_obj, created = Order.objects.get_or_create(
                owner=customer,
                order_status=Order.CART_SATGE
            )
            product = Product.objects.get(pk=product_id)
            ordered_item, created = OrderItem.objects.get_or_create(
                product=product,
                owner=cart_obj,
            )
            if created:
                ordered_item.quantity = quantity
            else:
                ordered_item.quantity += quantity
            ordered_item.save()
            return redirect('cart')
        except Exception as e:
            return HttpResponseServerError(str(e))
    else:
        return HttpResponseServerError("Invalid request method")

def remove_item_from_cart(request, pk):
    item = OrderItem.objects.get(pk=pk)
    if item:
        item.delete()
    return redirect('cart')

def payment_view(request):
    if request.method == 'POST':
       
        products = []
        i = 1
        while request.POST.get(f'product_title_{i}', None):
            product = {
                'title': request.POST.get(f'product_title_{i}'),
                'price': request.POST.get(f'product_price_{i}'),
                'quantity': request.POST.get(f'product_quantity_{i}')
            }
            products.append(product)
            i += 1
        
        request.session['products'] = products
        request.session['subtotal'] = request.POST.get('subtotal', None)
        request.session['tax'] = request.POST.get('tax', None)
        request.session['total'] = request.POST.get('total', None)
        request.session['hidden_name'] = request.POST.get('name', None)  # Changed here

        context = {
            'subtotal': request.POST.get('subtotal', None),
            'tax': request.POST.get('tax', None),
            'total': request.POST.get('total', None),
            'hidden_name': request.POST.get('name', None),  # Changed here
        }
        return render(request, 'payment.html', context)
    else:
        return redirect('cart')

def bill_receipt(request):
    if request.method == 'POST':
        products = request.session.get('products', [])
        context = {
            'products': products,
            'sub': request.session.get('subtotal', None),
            'tax': request.session.get('tax', None),
            'total': request.session.get('total', None),
            'hidden_name': request.session.get('hidden_name', None),  # Ensure correct key
        }
        return render(request, 'bill_receipt.html', context)
    else:
        return redirect('cart')


