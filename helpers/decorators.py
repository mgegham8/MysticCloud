from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect


def profile_decorator(func):
    """
    Ensures that the logged-in user can only access their own profile page.
    """

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # Compare the logged-in user's Primary Key with the PK provided in the URL.
        # We convert both to strings to ensure a reliable comparison.
        if str(request.user.pk) != str(kwargs.get("pk")):
            messages.error(request, "Invalid attempt! You cannot access this profile.")
            return redirect("home:home")
        return func(request, *args, **kwargs)

    return wrapper


def own_restaurant_product(product_field: str):
    """
    Verifies if the requested product belongs to a restaurant owned by the current user.
    Useful for protecting inventory in large databases (e.g., 10,000+ items).
    """

    def wrapper_func(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            product_id = kwargs.get("pk")

            # Efficient database lookup using exists() to check permission
            # without loading the entire object into memory.
            user_owns_product = request.user.restaurant_set.filter(
                **{f"{product_field}__id": product_id}
            ).exists()

            if not user_owns_product:
                messages.error(request, "You don't have permission to perform this action!")
                return redirect("menu:menu_list")

            return func(request, *args, **kwargs)

        return wrapper

    return wrapper_func