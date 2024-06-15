from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import OrderForm
from profiles.models import UserProfile, UserAddress

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, 'Your cart is empty!')
        return redirect(reverse('products'))

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

    template = 'checkout/checkout.html'
    context = {
        'order_form': form,
    }

    return render(request, template, context)
