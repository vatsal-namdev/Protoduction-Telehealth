from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse
from .models import Subscription  # Adjust based on your actual model location

def subscription_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Check if user is authenticated and has an active subscription
        if request.user.is_authenticated:
            try:
                subscription = Subscription.objects.get(user=request.user, is_active=True)
                return view_func(request, *args, **kwargs)  # Proceed to the view function
            except Subscription.DoesNotExist:
                return redirect(reverse('plan'))  # Redirect to plan page if no active subscription

        # Redirect to plan page if user is not authenticated
        return redirect(reverse('plan'))

    return wrapper
