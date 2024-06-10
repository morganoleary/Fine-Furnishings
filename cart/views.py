from django.shortcuts import render

# Create your views here.
def cart(request):
    """ A view to return the shopping cart/basket page """

    return render(request, 'cart/shopping_cart.html')
