from django.shortcuts import render, redirect, HttpResponse
from math import ceil
from datetime import datetime as dt
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import ContactUs, Product, Reviews, Checkout, Order, Payment,CartItem  
from io import BytesIO
from xhtml2pdf import pisa
import logging
import json


logger = logging.getLogger(__name__)

def home(request) -> HttpResponse:
    """
    Handles the homepage view.
    """
    selected_category = request.POST.get('my_cat', 'Drinks')
    all_products = []
    categories = Product.objects.values('category', 'product_id')
    unique_categories = {item['category'] for item in categories}

    for category in unique_categories:
        if category == selected_category:
            products = Product.objects.filter(category=category)
            n = len(products)
            n_slides = n // 4 + ceil((n / 4) - (n // 4))
            all_products.append([products, range(1, n_slides), n_slides])

    user_reviews = Reviews.objects.all()
    context = {
        'all_products': all_products,
        'user_reviews': user_reviews,
    }
    return render(request, "home/index.html", context)


def about(request) -> HttpResponse:
    """
    Handles the about us page view.
    """
    return render(request, "home/aboutus.html")


def contact(request) -> HttpResponse:
    """
    Handles the contact us page view and form submission.
    """
    if request.method == "POST":
        try:
            name = request.POST.get('help_name')
            email = request.POST.get('help_email')
            description = request.POST.get('help_desc')
            contact = ContactUs(name=name, email=email, desc=description, date=dt.today())
            contact.save()
            messages.success(request, 'Your message has been sent successfully!')
        except Exception as e:
            logger.error(f"Error in contact form submission: {e}")
            messages.error(request, 'Error sending message. Please try again.')
    
    return render(request, "home/contactus.html")


def tracker(request) -> HttpResponse:
    """
    Handles the tracker page view.
    """
    return render(request, 'home/tracker.html')

def food_view(request):
    """
    Handles the food page view and adding items to the cart.
    """
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action', 'add')  # Default action is 'add'

        if product_id and action:
            try:
                product = Product.objects.get(id=product_id)
                cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
                if action == 'add' and created:
                    messages.success(request, f"{product.product_name} added to your cart!")
                elif action == 'remove' and not created:
                    cart_item.delete()
                    messages.success(request, f"{product.product_name} removed from your cart!")
                elif action == 'increase' and not created:
                    cart_item.quantity += 1
                    cart_item.save()
                    messages.success(request, f"Quantity of {product.product_name} increased!")
                elif action == 'decrease' and not created and cart_item.quantity > 1:
                    cart_item.quantity -= 1
                    cart_item.save()
                    messages.success(request, f"Quantity of {product.product_name} decreased!")
            except Product.DoesNotExist:
                messages.error(request, "Product not found.")

        return redirect('cart')  # Redirect back to cart after updating

    all_products = Product.objects.all()
    print("Cart Items with Total: ", all_products)  # Debugging line

    context = {
        'food': all_products,
        'cart_count': CartItem.objects.filter(user=request.user).count(),
    }
    return render(request, 'home/food.html', context)

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login page if the user is not logged in

    # Fetch cart items and count for the logged-in user
    cart_items = CartItem.objects.filter(user=request.user)
    print("Cart Items: ", cart_items)  # Debugging line
    cart_count = cart_items.count()

    # Calculate total price and total items for each cart item
    total_price = 0
    total_items = 0
    cart_items_with_total = []  # To hold cart items with their calculated total price

    for item in cart_items:
        item_total = item.product.price * item.quantity
        total_price += item_total
        total_items += item.quantity
        cart_items_with_total.append({'item': item, 'item_total': item_total})

    print("Cart Items with Total: ", cart_items_with_total)  # Debugging line

    return render(request, 'home/cart.html', {
        'cart_items': cart_items_with_total,
        'total_price': total_price,
        'total_items': total_items,
        'cart_count': cart_count
    })

    
# Add or update a cart item
def update_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')
        product = Product.objects.get(id=product_id)

        # Add or update the cart item
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product
        )
        if not created:  # If item already exists, update the quantity
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1
            cart_item.save()

        return JsonResponse({'message': 'Cart updated', 'cart_count': CartItem.objects.filter(user=request.user).count()})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def checkout(request):
    """
    Handles the checkout page view.
    """    
    try:
        cart_items = CartItem.objects.filter(user=request.user)
        cart_count = cart_items.count()

        # Calculate total price and total items for each cart item
        total_price = 0
        total_items = 0
        cart_items_with_total = []  # To hold cart items with their calculated total price

        for item in cart_items:
            item_total = item.product.price * item.quantity
            total_price += item_total
            total_items += item.quantity
            cart_items_with_total.append({'item': item, 'item_total': item_total})

        if request.method == "POST":
            # Retrieve form data
            name = request.POST.get('name')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            zipcode = request.POST.get('zipcode')
            country = request.POST.get('country')

            # Create Checkout instance
            checkout_instance = Checkout.objects.create(
                user=request.user,
                name=name,
                email=email,
                address=address,
                city=city,
                state=state,
                zipcode=zipcode,
                country=country
            )

            # Record payment
            Payment.objects.create(
                checkout=checkout_instance,
                payment_method='PayPal',  # Replace with dynamic selection if needed
                payment_date=dt.now(),
                amount=total_price
            )

            # Clear the cart
            cart_items.delete()

    except Exception as e:
        logger.error(f"Error during checkout: {e}")
        # Optionally, you could also add a message for the user if needed
        # messages.error(request, "An error occurred during checkout. Please try again.")

    return render(request, 'home/checkout.html', {
        'cart_items': cart_items_with_total,
        'total_price': total_price,
        'total_items': total_items,
        'cart_count': cart_count,
    })

def review_form(request) -> HttpResponse:
    """
    Handles the review form submission.
    """
    if request.method == "POST":
        try:
            review_desc = request.POST.get('user_review', 'default')
            review_name = request.user.username
            my_review = Reviews(reviewer_name=review_name, review=review_desc, review_date=dt.today())
            my_review.save()
            messages.success(request, 'Your review has been submitted successfully!')
        except Exception as e:
            logger.error(f"Error submitting review: {e}")
            messages.error(request, 'Error submitting review. Please try again.')
    
    return render(request, "home/review.html")
