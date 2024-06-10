from decimal import Decimal
from django.conf import settings

def cart_contents(request):

    cart_items= []
    total = 0
    product_count = 0
    delivery = Decimal(settings.STANDARD_DELIVERY_FEE)

    order_total = total + delivery

    context = {
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': settings.STANDARD_DELIVERY_FEE,
        'order_total': order_total
    }

    return context