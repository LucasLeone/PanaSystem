"""Tokens middlewares."""

# Django
from django.http import JsonResponse

# Django REST Framework
from rest_framework_simplejwt.tokens import AccessToken

# Models
from panasystem.users.models import BlacklistedAccessToken


class BlacklistAccessTokenMiddleware:
    """Blacklist access token middleware."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                token_type, token = auth_header.split()
                if token_type == 'Bearer':
                    access_token = AccessToken(token)
                    if BlacklistedAccessToken.objects.filter(token=str(access_token)).exists():
                        return JsonResponse({"detail": "Access token has been blacklisted"}, status=401)
            except Exception as e:
                pass
        response = self.get_response(request)
        return response