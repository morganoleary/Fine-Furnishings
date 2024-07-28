from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.
def cart(request):
    """ A view to return the shopping cart/basket page """

    return render(request, 'cart/shopping_cart.html')


def add_to_cart(request, item_id):
    """ A view to add a specific quantity of a specific product to the cart """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'bedframe_size' in request.POST:
        size = request.POST['bedframe_size']
    cart = request.session.get('cart', {})

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]['bedframes_by_size'].keys():
                cart[item_id]['bedframes_by_size'][size] += quantity
                messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {cart[item_id]["bedframes_by_size"][size]} ')
            else:
                cart[item_id]['bedframes_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your cart!')
        else:
            cart[item_id] = {'bedframes_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your cart!')
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}.')
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.name} to your cart!')

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def update_cart(request, item_id):
    """ A view to update the quantity of a specific product within the cart """

    product = get_object_or_404(Product, pk=item_id)
    item_id = str(item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'bedframe_size' in request.POST:
        size = request.POST['bedframe_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['bedframes_by_size'][size] = quantity
            messages.success(request, f'Updated size {size.upper()} {product.name} quantity to {cart[item_id]["bedframes_by_size"][size]} ')
        else:
            del cart[item_id]['bedframes_by_size'][size]
            if not cart[item_id]['bedframes_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart.')
    else:
        if quantity > 0:
            cart[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {cart[item_id]}.')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart.')

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ A view to remove a specific product from the cart """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'bedframe_size' in request.POST:
            size = request.POST['bedframe_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['bedframes_by_size'][size]
            if not cart[item_id]['bedframes_by_size']:
                cart.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your cart.')
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart.')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)