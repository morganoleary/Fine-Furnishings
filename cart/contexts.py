from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def cart_contents(request):
    """ 
    A context function to calculate & return the contents of the shopping cart
    """
    cart_items= []
    total = 0
    product_count = 0
    delivery = Decimal(settings.STANDARD_DELIVERY_FEE)
    cart = request.session.get('cart', {})

    for item_id, product_data in cart.items():
        if isinstance(product_data, int):
            product = get_object_or_404(Product, pk=item_id)
            total += product_data * product.price
            product_count += product_data
            cart_items.append({
                'item_id': item_id,
                'quantity': product_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in product_data['bedframes_by_size'].items():
                total += quantity * product.price
                product_count += quantity
                cart_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'size': size,
                })

    order_total = total + delivery

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': settings.STANDARD_DELIVERY_FEE,
        'order_total': order_total
    }

    return context