from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from .models import Order, OrderItems
from products.models import Product
from profiles.models import UserAddress, UserProfile

import stripe
import json
import time

# Webhook handler implemented with Boutique Ado Walkthrough - Stripe Part 10
class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """
        Send the user a confirmation email
        """
        user_email = order.user_email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})
        
        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [user_email]
        )

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

        # Added check to prevent duplicate orders
        if Order.objects.filter(stripe_pid=pid).exists():
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Order already processed',
                status=200)

        order_exists = False
        attempt = 1
        while attempt <= 5:
            try:
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
                attempt += 1
                time.sleep(1)
            except UserAddress.DoesNotExist:
                break

        if order_exists:
            self._send_confirmation_email(order)
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | SUCCESS: Verified order already in database', status=200)
        else:
            order = None
            try:
                address, created = UserAddress.objects.get_or_create(
                    street_address_1=shipping_details.address.line1,
                    street_address_2=shipping_details.address.line2,
                    town_city=shipping_details.address.city,
                    post_code=shipping_details.address.postal_code,
                    country=shipping_details.address.country,
                )

                # Find the user profile based on the email
                user_profile = None
                try:
                    user_profile = UserProfile.objects.get(user_id__email=billing_details.email)
                except UserProfile.DoesNotExist:
                    pass

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
                        continue
            except Exception as e:
                if order:
                    order.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)
        self._send_confirmation_email(order)
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