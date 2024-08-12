from django.contrib.auth.mixins import LoginRequiredMixin


class UserRequiredMixin(LoginRequiredMixin):
    """Mixin to require user authentication."""

    login_url = "/login/"
    redirect_field_name = "next"


class CustomMixin(UserRequiredMixin):
    """Custom mixin with additional functionality."""

    # Add your custom functionality here
    pass
