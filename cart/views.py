from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product

# Create your views here.
def cart(request):
    """ A view to return the shopping cart/basket page """

    return render(request, 'cart/shopping_cart.html')


def add_to_cart(request, item_id):
    """ A view to add a specific quantity of a specific product to the cart """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'bedframe_size' in request.POST:
        size = request.POST['bedframe_size']
    cart = request.session.get('cart', {})

    if size:
        if item_id in list(cart.keys()):
            if size in cart[item_id]['bedframes_by_size'].keys():
                cart[item_id]['bedframes_by_size'][size] += quantity
            else:
                cart[item_id]['bedframes_by_size'][size] = quantity
        else:
            cart[item_id] = {'bedframes_by_size': {size: quantity}}
    else:
        if item_id in list(cart.keys()):
            cart[item_id] += quantity
        else:
            cart[item_id] = quantity
            messages.success(request, f'Added {product.name} to your cart!')

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def update_cart(request, item_id):
    """ A view to update the quantity of a specific product within the cart """

    item_id = str(item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'bedframe_size' in request.POST:
        size = request.POST['bedframe_size']
    cart = request.session.get('cart', {})

    if size:
        if quantity > 0:
            cart[item_id]['bedframes_by_size'][size] = quantity
        else:
            del cart[item_id]['bedframes_by_size'][size]
            if not cart[item_id]['bedframes_by_size']:
                cart.pop(item_id)
    else:
        if quantity > 0:
            cart[item_id] = quantity
        else:
            cart.pop(item_id)

    request.session['cart'] = cart
    return redirect(reverse('cart'))


def remove_from_cart(request, item_id):
    """ A view to remove a specific product from the cart """

    product = Product.objects.get(pk=item_id)
    try:
        size = None
        if 'bedframe_size' in request.POST:
            size = request.POST['bedframe_size']
        cart = request.session.get('cart', {})

        if size:
            del cart[item_id]['bedframes_by_size'][size]
            if not cart[item_id]['bedframes_by_size']:
                cart.pop(item_id)
        else:
            cart.pop(item_id)
            messages.success(request, f'Removed {product.name} from your cart.')

        request.session['cart'] = cart
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)