from rest_framework.permissions import BasePermission, IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import BasePermission

from rest_framework_simplejwt.authentication import api_settings
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError

HTTP_AUTHORIZATION = "HTTP_AUTHORIZATION"

class CustomAuth(BasePermission):
    def has_permission(self, request, view):
        raw_token = self._extract_token(request)
        if raw_token:
            return self._validate_token(raw_token)
        else:
            return False

    def _extract_token(self, request):
        if HTTP_AUTHORIZATION in request.META.keys():
            return request.META[HTTP_AUTHORIZATION].split()[-1]
        else:
            return None

    def _validate_token(self, raw_token):
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                if AuthToken(raw_token):
                    return True
            except TokenError as e:
                messages.append(
                    {
                        "token_class": AuthToken.__name__,
                        "token_type": AuthToken.token_type,
                        "message": e.args[0],
                    }
                )
        if messages:
            raise AuthenticationFailed(messages, code="token_invalid")
        else:
            raise AuthenticationFailed("Invalid token", code="invalid_token")

    def _handle_exception(self, exception):
        if isinstance(exception, TokenError):
            return AuthenticationFailed(exception.args[0], code="token_error")
        else:
            return AuthenticationFailed(str(exception), code="unknown_error")



# Custom permission class
class CustomPermission(BasePermission):
    def has_permission(self, request, view):
        # Add your custom permission logic here
        return True


# Example usage of built-in permissions
class ExampleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Add your code logic here
        return Response("GET request")

    def post(self, request):
        # Add your code logic here
        return Response("POST request")


# Example usage of custom permission
class CustomView(APIView):
    permission_classes = [CustomPermission]

    def get(self, request):
        # Add your code logic here
        return Response("GET request")

    def post(self, request):
        # Add your code logic here
        return Response("POST request")
