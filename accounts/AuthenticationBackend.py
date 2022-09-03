from django.conf import settings

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken

from .utils import enforce_csrf

class CustomAuthentication(JWTAuthentication):
    def authenticate(self, request):
        header = self.get_header(request)
        print(header)
        if header is not None:
            raw_token = self.get_raw_token(header)
        else:
            raw_token = request.COOKIES.get(
                settings.SIMPLE_JWT.get('AUTH_COOKIE', None), None
            )

        if raw_token is None:
            return None

        # if refresh_token:
        #     new_tokens = RefreshToken(refresh_token)
        #     raw_token = str(new_tokens.access_token)
        validated_token = self.get_validated_token(raw_token)
        enforce_csrf(request)
        return self.get_user(validated_token), validated_token
