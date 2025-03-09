from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Order, OrderItem, Profile, Product,Payment
import stripe
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY


class PlaceOrderView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return redirect('create_profile')

        # Get or create an order for the profile
        order, created = Order.objects.get_or_create(customer=profile)

        try:
            product = Product.objects.get(id=kwargs['pk'])
        except Product.DoesNotExist:
            return redirect('home')  # Product does not exist, redirect to home

        # Get or create order item
        order_item, item_created = OrderItem.objects.get_or_create(order=order, product=product, defaults={'quantity': 1, 'subtotal': product.price})

        if not item_created:
            order_item.quantity += 1
            order_item.subtotal = product.price * order_item.quantity

            order_item.save()  # Save the updated order item


        return redirect('home')

# cart view
class CartView(LoginRequiredMixin,View):
    def get(self,request):
        try:
            profile=Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            return redirect('profile')

        orders = Order.objects.get(customer=profile)
        order_item_list = OrderItem.objects.filter(order=orders)

        context = {
            'orders': order_item_list,
            'total_amount':orders.total_amount
        }
        return render(request,'order/order.html',context)



def create_checkout_session(request):
    """Creates a Stripe payment session."""
    profile=Profile.objects.get(user=request.user)
    order = get_object_or_404(Order, customer=profile)

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': f'Order {order.id}'},
                    'unit_amount': int(order.total_amount * 100),  # Stripe works with cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment/success/{order.id}/'),
            cancel_url=request.build_absolute_uri(f'/payment/cancel/{order.id}/'),
        )

        # Save Payment Information
        payment = Payment.objects.create(
            order=order,
            amount=order.total_amount,
            stripe_charge_id=checkout_session['id'],
            status="Pending"
        )

        return JsonResponse({'session_id': checkout_session.id})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

