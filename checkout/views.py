from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import OrderForm
from .models import Order, OrderItems
from profiles.models import UserProfile, UserAddress
from products.models import Product
from cart.contexts import cart_contents

import stripe

@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'street_address_1': request.POST['street_address1'],
            'street_address_2': request.POST['street_address2'],
            'town_city': request.POST['town_or_city'],
            'county': request.POST['county'],
            'post_code': request.POST['postcode'],
            'country': request.POST['country'],
        }
        form = OrderForm(form_data)
        if form.is_valid():
            order = form.save(commit=False)
            user_profile = request.user.userprofile
            order.user_profile = user_profile
            order.delivery_charge = 30
            order.save()

            if request.POST.get('save-info'):
                address_data = {
                    'street_address_1': form.cleaned_data['street_address1'],
                    'street_address_2': form.cleaned_data['street_address2'],
                    'town_city': form.cleaned_data['town_or_city'],
                    'county': form.cleaned_data['county'],
                    'post_code': form.cleaned_data['postcode'],
                    'country': form.cleaned_data['country'],
                }
                UserAddress.objects.update_or_create(
                    user_profile=user_profile,
                    defaults=address_data,
                )

            for item_id, product_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(product_data, int):
                        order_items = OrderItems(
                            order=order,
                            product=product,
                            quantity=product_data,
                        )
                        order_items.save()
                    else:
                        for size, quantity in product_data['bedframes_by_size'].items():
                            order_items = OrderItems(
                                order=order,
                                product=product,
                                quantity=quantity,
                                size=size,
                            )
                            order_items.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your shopping cart wasn't found in our database. "
                        "Please contact us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('order_confirmation', args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. Please double check your information.')
    else:
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

        user_profile = request.user.userprofile
        form = OrderForm(initial={
            'full_name': user_profile.user.get_full_name(),
            'email': user_profile.user.email,
            'phone_number': user_profile.default_phone_number,
            'street_address_1': user_profile.default_street_address_1,
            'street_address_2': user_profile.default_street_address_2,
            'town_city': user_profile.default_town_city,
            'county': user_profile.default_county,
            'post_code': user_profile.default_post_code,
            'country': user_profile.default_country,
        })

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def order_confirmation(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Order successfully processed! Your order number is {order_number}. A confirmation email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/order_confirmation.html'
    context = {
        'order_number': order_number,
    }
    return render(request, template, context)
