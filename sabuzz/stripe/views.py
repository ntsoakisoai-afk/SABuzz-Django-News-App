import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.views import View
from sabuzz.models import Premium

class SubscribeView(View):
    def get(self, request):
        return render(request, 'stripe/subscribe.html', {
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY
        })

class CreateCheckoutSessionView(View):
    def post(self, request):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': settings.STRIPE_PRICE_ID,
                'quantity': 1,
            }],
            mode='Subscription',
            success_url=request.build_absolute_uri('/payment-success/'),
            cancel_url=request.build_absolute_uri('/payment-cancel/'),
            customer_email = request.user.email,
        )

        return redirect(checkout_session.url)

class PaymentSuccessView(View):
    def get(self, request):
        return render(request, 'sabuzz/payment_success.html')

class PaymentCancelView(View):
    def get(self, request):
        return render(request, 'sabuzz/payment_cancel.html')



