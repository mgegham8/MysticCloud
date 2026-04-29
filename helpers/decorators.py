from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse


def profile_decorator(func):
    """
    Ensures that the logged-in user can only access their own profile.
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # request is usually the first argument in Django views
        # Compare logged-in user's PK with the PK from the URL
        if request.user.pk != kwargs.get("pk"):
            messages.error(request, "Invalid attempt!")
            return redirect("home:home")  # Using namespace for consistency
        return func(request, *args, **kwargs)

    return wrapper


def own_restaurant_product(product: str):
    """
    Checks if the product belongs to a restaurant owned by the current user.
    """

    def wrapper_func(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            product_id = kwargs.get("pk")

            # Efficient lookup using exists() to check permission
            user_owns_product = request.user.restaurant_set.filter(
                **{f"{product}__id": product_id}
            ).exists()

            if not user_owns_product:
                messages.error(request, "You don't have permission to perform this action!")
                return redirect("menu:menu_list")  # Redirecting to a more relevant page

            return func(request, *args, **kwargs)

        return wrapper

    return wrapper_func