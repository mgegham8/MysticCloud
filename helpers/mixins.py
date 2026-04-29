from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from helpers.decorators import profile_decorator

class OwnProfileMixin:
    """
    Mixin to ensure that only the authenticated owner of the profile
    can access the view.
    """
    @method_decorator(login_required)
    @method_decorator(profile_decorator)
    def dispatch(self, request, *args, **kwargs):
        # The dispatch method is the entry point for all Django Class-Based Views.
        # By decorating it, we protect all HTTP methods (GET, POST, etc.) at once.
        return super().dispatch(request, *args, **kwargs)