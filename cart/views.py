from django.shortcuts import render, redirect

# Create your views here.
def cart(request):
    """ A view to return the shopping cart/basket page """

    return render(request, 'cart/shopping_cart.html')

def add_to_cart(request, item_id):
    """ A view to add a specific quantity of a specific product to the cart """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
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

    request.session['cart'] = cart
    return redirect(redirect_url)