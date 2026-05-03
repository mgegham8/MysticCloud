from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from helpers.decorators import profile_decorator

class OwnProfileMixin:
    """
    Mixin to ensure that only the authenticated owner of the profile
    can access the view. Used in Class-Based Views.
    """
    @method_decorator(login_required)
    @method_decorator(profile_decorator)
    def dispatch(self, request, *args, **kwargs):
        # The dispatch method handles all incoming requests.
        # Decorating it ensures all HTTP methods (GET, POST, etc.) are protected.
        return super().dispatch(request, *args, **kwargs)