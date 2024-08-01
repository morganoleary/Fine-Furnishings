from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib import messages
from .models import UserProfile, UserAddress, Wishlist
from products.models import Product
from checkout.models import Order
from .forms import UserProfileForm, UserAddressForm
from django.forms import modelformset_factory

# Create your views here.

def user_profile(request):
    """
    View to display the profile of a logged in user.
    """

    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user_id=request.user)
        # Returns the address formset for the User Address model
        AddressFormSet = modelformset_factory(UserAddress, form=UserAddressForm, extra=1, can_delete=True, max_num=5)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            address_formset = AddressFormSet(request.POST, queryset=user_profile.addresses.all())

            if form.is_valid() and address_formset.is_valid():
                form.save()
                addresses = address_formset.save(commit=False)
                for address in addresses:
                    address.user_profile = user_profile
                    address.save()
                # Handle deletions of address
                for address in address_formset.deleted_objects:
                    address.delete()
                return redirect('user_profile')
        else:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
            form = UserProfileForm(instance=user_profile, initial=initial_data)
            address_formset = AddressFormSet(queryset=user_profile.addresses.all())

        context = {
            'user_profile': user_profile,
            'form': form,
            'address_formset': address_formset,
                    }
        return render(request, "profiles/user_profile.html", context)
    else:
        return redirect('login')


@login_required
def user_wishlist(request):
    """
    View to render the user's wishlist.
    """
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    wishlist_items = Wishlist.objects.filter(user_profile=profile).select_related('product')
    context = {'wishlist': wishlist_items}
    return render(request, 'profiles/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """
    View to add a product from the user's wishlist.
    """
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    product = get_object_or_404(Product, id=product_id)

    if Wishlist.objects.filter(user_profile=profile, product=product).exists():
        messages.info(request, f'{product.name} is already in your wishlist.')
    else:
        Wishlist.objects.create(user_profile=profile, product=product)
        messages.success(request, f'Added {product.name} to your wishlist.')

    return redirect('user_wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    """
    View to remove a product from the user's wishlist.
    """
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    product = get_object_or_404(Product, id=product_id)

    wishlist_item = Wishlist.objects.filter(user_profile=profile, product=product).first()
    if wishlist_item:
        wishlist_item.delete()
        messages.success(request, f'Removed {product.name} from your wishlist.')
    else:
        messages.error(request, f'{product.name} is not in your wishlist.')

    return redirect('user_wishlist')


@login_required
def delete_user_profile(request):
    """
    View to delete the user's profile.
    """
    user_profile = get_object_or_404(UserProfile, user_id=request.user)

    if request.method == 'POST':
        try:
            # Retain addresses but remove from user's profile
            user_profile.addresses.all().update(user_profile=None)
            # Store necessary user details in orders before deleting user
            orders = Order.objects.filter(user_profile=user_profile)
            for order in orders:
                order.user_name = request.user.get_full_name()
                order.user_email = request.user.email
                order.user_phone = user_profile.phone
                order.save()
            # Filter user's orders and set user's profile on orders to none
            Order.objects.filter(user_profile=user_profile).update(user_profile=None)
            # Delete the user's profile
            user_profile.delete()
            # Delete the user account
            request.user.delete()
            # Log the user out
            logout(request)

            messages.success(request, "Your profile has been deleted successfully.")
            return redirect('home')
        except Exception as e:
            messages.error(request, "An error occurred while deleting your profile.")
            return redirect('home')

    return render(request, 'profiles/delete_profile.html')


@login_required
def order_history(request):
    """
    View to render the user's order history.
    """
    user_profile = get_object_or_404(UserProfile, user_id=request.user)
    orders = Order.objects.filter(user_profile=user_profile).order_by('-order_date')

    context = {
        'orders': orders
    }

    return render(request, 'profiles/order_history.html', context)