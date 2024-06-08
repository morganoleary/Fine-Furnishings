from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from products.models import Product
from .forms import UserProfileForm

# Create your views here.

def user_profile(request):
    """
    View to display the profile of a logged in user.
    Displays an individual instance of
        :model: `UserProfile`
    """

    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user_id=request.user)

        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                return redirect('user_profile')
        else:
            form = UserProfileForm(instance=user_profile)

        context = {
            'user_profile': user_profile,
            'form': form
                    }
        return render(request, "profiles/user_profile.html", context)
    else:
        return redirect('login')


@login_required
def user_wishlist(request):
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    wishlist = profile.wishlist.all()
    return render(request, 'profiles/wishlist.html', {'wishlist': wishlist})

@login_required
def add_to_wishlist(request, product_id):
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    product = get_object_or_404(Product, id=product_id)

    if product in profile.wishlist.all():
        messages.info(request, f'{product.name} is already in your wishlist.')
    else:
        profile.wishlist.add(product)
        messages.success(request, f'Added {product.name} to your wishlist.')

    return redirect('user_wishlist')


@login_required
def remove_from_wishlist(request, product_id):
    try:
        profile = UserProfile.objects.get(user_id=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'You need to be logged in to view your wishlist. Please log in or register.')
        return redirect('account_login')

    product = get_object_or_404(Product, id=product_id)

    if product in profile.wishlist.all():
        profile.wishlist.remove(product)
        messages.success(request, f'Removed {product.name} from your wishlist.')
    else:
        messages.error(request, f'{product.name} is not in your wishlist.')

    return redirect('user_wishlist')