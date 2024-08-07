from django.http import HttpResponse

from .models import Order, OrderItems
from products.models import Product
from profiles.models import UserAddress, UserProfile

import stripe
import json
import time

import logging

logger = logging.getLogger(__name__)

# Webhook handler implemented with Boutique Ado Walkthrough - Stripe Part 10
class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        pid = intent.id
        cart = intent.metadata.cart
        save_info = intent.metadata.save_info

        # Get the Charge object
        stripe_charge = stripe.Charge.retrieve(
            intent.latest_charge
        )

        billing_details = stripe_charge.billing_details
        shipping_details = intent.shipping
        order_total = round(stripe_charge.amount / 100, 2)

        # Clean data in the shipping details
        for field, value in shipping_details.address.items():
            if value == "":
                shipping_details.address[field] = None
        
        # Ensure country field is set to "IE"
        shipping_details.address.country = "IE"

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                # Debugging
                logger.debug(f"Attempt {attempt}: Looking for address with details: "
                             f"{shipping_details.address.line1}, "
                             f"{shipping_details.address.line2}, "
                             f"{shipping_details.address.city}, "
                             f"{shipping_details.address.postal_code}, "
                             f"{shipping_details.address.country}")
                
                address = UserAddress.objects.get(
                    street_address_1__iexact=shipping_details.address.line1,
                    street_address_2__iexact=shipping_details.address.line2,
                    town_city__iexact=shipping_details.address.city,
                    post_code__iexact=shipping_details.address.postal_code,
                    country__iexact=shipping_details.address.country,
                )
                order = Order.objects.get(
                    user_name__iexact=shipping_details.name,
                    user_email__iexact=billing_details.email,
                    user_phone__iexact=shipping_details.phone,
                    address=address,
                    order_total=order_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                order_exists = True
                break
            except Order.DoesNotExist:
                logger.debug(f"Order does not exist on attempt {attempt}.")
                attempt += 1
                time.sleep(1)
            except UserAddress.DoesNotExist:
                logger.error(f"UserAddress matching query does not exist. "
                             f"Details: {shipping_details.address.line1}, "
                             f"{shipping_details.address.line2}, "
                             f"{shipping_details.address.city}, "
                             f"{shipping_details.address.postal_code}, "
                             f"{shipping_details.address.country}")
                break
        if order_exists:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database', status=200)
        else:
            # order = None
            try:
                address, created = UserAddress.objects.get_or_create(
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    town_city=shipping_details.address.city,
                    post_code=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                )
                # Log if the address was created or retrieved
                if created:
                    logger.info(f"Created new address: {address}")
                else:
                    logger.info(f"Retrieved existing address: {address}")

                # Find the user profile based on the email
                user_profile = None
                try:
                    user_profile = UserProfile.objects.get(user_id__email=billing_details.email)
                except UserProfile.DoesNotExist:
                    logger.error(f"UserProfile matching email {billing_details.email} does not exist.")

                # Create order
                order = Order.objects.create(
                    user_profile=user_profile,
                    user_name=shipping_details.name,
                    user_email=billing_details.email,
                    user_phone=shipping_details.phone,
                    address=address,
                    order_total=order_total,
                    original_cart=cart,
                    stripe_pid=pid,
                )
                for item_id, product_data in json.loads(cart).items():
                    try:
                        product = Product.objects.get(id=item_id)
                        if isinstance(product_data, int):
                            order_item = OrderItems(
                                order=order,
                                product=product,
                                quantity=product_data,
                            )
                            order_item.save()
                        else:
                            for size, quantity in product_data['bedframes_by_size'].items():
                                order_item = OrderItems(
                                    order=order,
                                    product=product,
                                    quantity=quantity,
                                    bedframe_size=size,
                                )
                                order_item.save()
                    except Product.DoesNotExist:
                        logger.error(f"Product with ID {item_id} does not exist.")
                        continue
            except Exception as e:
                logger.error(f'Error handling payment_intent.succeeded: {e}')
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        return HttpResponse(
            content=f'Webhook received: {event["type"]} | SUCCESS: Created order in webhook',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)