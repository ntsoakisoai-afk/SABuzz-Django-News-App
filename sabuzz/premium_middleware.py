from django.shortcuts import redirect
from django.urls import reverse
from .models import Premium

class PremiumRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):

        premium_paths = [
            '/videos/',
            '/podcasts/',
        ]
        
        #Check if user is accessing premium content
        if any(request.path.startswith(p) for p in premium_paths):

            #user not logged in - redirect to login with next parameter
            if not request.user.is_authenticated:
                return redirect(f"{reverse('login')}?next={request.path}")
            
            #Check if premium subscription exists
            subscription = Premium.objects.filter(
                user=request.user,
                is_active=True
                ).first()
                
            if not subscription:
                return redirect('create_chackout') # takes uder to Stripe subcription page

        return self.get_response(request)