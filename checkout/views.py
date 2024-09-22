from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

from .forms import OrderForm
from .models import Order, OrderItems
from profiles.models import UserProfile, UserAddress
from products.models import Product
from cart.contexts import cart_contents

import stripe
import json

@require_POST
def cache_checkout_data(request):
    """
    View to get meta data if user chooses to 'save info'.
    Implemented with the Boutiqe Ado Walkthrough - Stripe Part 13
    """
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


@login_required
def checkout(request):
    """ 
    A view to handle the checkout process using Stripe payments
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    intent = None
    user_profile = request.user.userprofile  # Assuming user is logged in and has a profile

    cart = request.session.get('cart', {})
    user_addresses = []

    if request.method == 'POST':
        form = OrderForm(data=request.POST, user_profile=user_profile)
        if form.is_valid():
            pid = request.POST.get('client_secret').split('_secret')[0]
            # Check if an order with the same stripe_pid already exists
            existing_order = Order.objects.filter(stripe_pid=pid).first()
            if existing_order:
                messages.error(request, 'This order has already been processed.')
                return redirect(reverse('order_confirmation', args=[existing_order.order_number]))

            # Create order but don't save until payment is confirmed
            order = form.save(commit=False)
            order.user_profile = user_profile

            # Set user details
            order.user_name = form.cleaned_data.get('full_name')
            order.user_email = form.cleaned_data.get('email')
            order.user_phone = form.cleaned_data.get('phone_number')

            order.delivery_charge = 30
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)

            # Handle address
            address_id = form.cleaned_data.get('address_choices')
            if address_id:
                try:
                    address = UserAddress.objects.get(id=address_id)
                    order.address = address
                except UserAddress.DoesNotExist:
                    messages.error(request, 'Selected address does not exist.')
                    return redirect(reverse('checkout'))
            else:
                address_name = form.cleaned_data.get('address_name')
                address_data = {
                    'street_address_1': form.cleaned_data['street_address1'],
                    'street_address_2': form.cleaned_data['street_address2'],
                    'town_city': form.cleaned_data['town_or_city'],
                    'county': form.cleaned_data['county'],
                    'post_code': form.cleaned_data['postcode'],
                    'country': form.cleaned_data['country'] or 'IE',
                }

                user_address, created = UserAddress.objects.update_or_create(
                    user_profile=user_profile,
                    address_name=address_name,
                    defaults=address_data,
                )
                order.address = user_address

            try:
                # Save the order after the address is confirmed
                order.save()

                # Create order items
                for item_id, product_data in cart.items():
                    try:
                        product = Product.objects.get(id=item_id)
                        if isinstance(product_data, int):
                            order_item = OrderItems(
                                order=order,
                                product=product,
                                quantity=product_data,
                            )
                            order_item.save()
                        else:
                            for size, quantity in product_data['bedframes_by_size'].items():
                                order_item = OrderItems(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    bedframe_size=size,
                                )
                                order_item.save()

                    except Product.DoesNotExist:
                        messages.error(request, (
                            "One of the products in your shopping cart wasn't found in our database. "
                            "Please contact us for assistance!")
                        )
                        order.delete()
                        return redirect(reverse('cart'))

                # Clear cart after successful order processing
                if 'cart' in request.session:
                    del request.session['cart']

                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('order_confirmation', args=[order.order_number]))

            except Product.DoesNotExist:
                messages.error(request, (
                    "One of the products in your shopping cart wasn't found in our database. "
                    "Please contact us for assistance!")
                )
                order.delete()
                return redirect(reverse('cart'))
        else:
            messages.error(request, 'There was an error with your order. Please double check your information.')

    # Check if the cart is empty
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect(reverse('products'))

    current_cart = cart_contents(request)
    total = current_cart['order_total']
    stripe_total = round(total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    initial_data = {
        'full_name': request.user.get_full_name(),
        'email': request.user.email,
        'phone_number': user_profile.phone,
    }

    user_addresses = UserAddress.objects.filter(user_profile=user_profile)
    if user_addresses.exists():
        user_address = user_addresses.first()
        initial_data.update({
            'street_address1': user_address.street_address_1,
            'street_address2': user_address.street_address_2,
            'town_or_city': user_address.town_city,
            'county': user_address.county,
            'postcode': user_address.post_code,
            'country': user_address.country,
        })
    form = OrderForm(initial=initial_data, user_profile=user_profile)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'user_addresses': user_addresses,
        'order_form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret if intent else '',
    }

    return render(request, template, context)


def order_confirmation(request, order_number):
    """
    View to handle successful order checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    email = order.user_profile.user_id.email
    user_profile = order.user_profile
    address = order.address

    messages.success(request, f'Order successfully processed! Your order number is {order_number}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/order_confirmation.html'
    context = {
        'order': order,
        'order_number': order_number,
        'email': email,
        'address': address,
    }
    return render(request, template, context)
