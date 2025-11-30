from django.urls import path
from .views import (
    SubscribeView,
    CreateCheckoutSessionView,
    PaymentSuccessView,
    PaymentCancelView,
)
from .webhook_handler import stripe

urlpatterns = [
    path('subscribe/', SubscribeView.as_view(), name='subscribe'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('payment-success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('payment-cancel/', PaymentCancelView.as_view(), name='payment_cancel'),
    path('webhook/', stripe, name='stripe_webhook'),
]
