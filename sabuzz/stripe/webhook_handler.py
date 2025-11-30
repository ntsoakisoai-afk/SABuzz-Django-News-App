import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from sabuzz.models import Premium, User

@csrf_exempt
def stripe(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']

    event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )

    if event['type'] == 'customer.subscription.created':
        data = event['data']['object']
        email = data['customer_email']
        user = User.objects.get(email=email)

        Premium.objects.create(
            user=user,
            stripe_customer_id=data['customer'],
            stripe_subscription_id=data['id'],
            is_active=True
        )

        #Subscription cancelled
        if event['type'] == 'customer.subscription.deleted':
            data = event['data']['object']
            subscription_id = data['id']

            Premium.objects.filter(
                
                stripe_subscription_id=subscription_id
            ).update(is_active=False)

        return HttpResponse(status=200)
        