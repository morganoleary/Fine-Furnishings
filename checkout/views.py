from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .forms import OrderForm
from profiles.models import UserProfile, UserAddress
from cart.contexts import cart_contents

import stripe

@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

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

    print(intent)

    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = OrderForm(request.POST, user_profile=user_profile)
        if form.is_valid():
            order = form.save(commit=False)
            order.user_profile = user_profile
            # Fixed delivery charge
            order.delivery_charge = 30

            order.save()

            # If the "save-info" checkbox is checked, update the user's address details
            if request.POST.get('save-info'):
                address, created = UserAddress.objects.get_or_create(
                    user_profile=user_profile,
                    defaults={
                        'street_address_1': form.cleaned_data['street_address1'],
                        'street_address_2': form.cleaned_data['street_address2'],
                        'town_city': form.cleaned_data['town_or_city'],
                        'county': form.cleaned_data['county'],
                        'post_code': form.cleaned_data['postcode'],
                        'country': form.cleaned_data['country'],
                    }
                )
                if not created:
                    address.street_address_1 = form.cleaned_data['street_address1']
                    address.street_address_2 = form.cleaned_data['street_address2']
                    address.town_city = form.cleaned_data['town_or_city']
                    address.county = form.cleaned_data['county']
                    address.post_code = form.cleaned_data['postcode']
                    address.country = form.cleaned_data['country']
                    address.save()

            messages.success(request, 'Order successfully placed!')
            return redirect('order_confirmation', order_number=order.order_number)
        else:
            messages.error(request, 'There was an error with your form. Please double-check your information.')
    else:
        form = OrderForm(user_profile=user_profile)

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': form,
        'stripe_public_key': 'stripe_public_key',
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)
