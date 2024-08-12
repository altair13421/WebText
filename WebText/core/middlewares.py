from django.shortcuts import redirect

class LoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is authenticated
        if not request.user.is_authenticated:
            # Redirect to login page
            return redirect('login')

        response = self.get_response(request)
        return response