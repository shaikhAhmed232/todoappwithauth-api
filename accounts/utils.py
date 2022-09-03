from tabnanny import check
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import CSRFCheck

def get_tokens(user):
    tokens = RefreshToken.for_user(user)
    return {
        "refresh": str(tokens),
        'access': str(tokens.access_token), 
    }

def timedelta_to_seconds(timedelta):
    days = timedelta.days
    seconds = timedelta.seconds
    if (seconds == 0):
        seconds = days * 24 * 3600

    return seconds

def enforce_csrf(request):
    def dummy_get_response():
        return None
    check_csrf = CSRFCheck(dummy_get_response)
    check_csrf.process_request(request)

    reason = check_csrf.process_view(request, None, (), {})
    if reason:
        msg = f"CSRF FAILED {reason}"
        raise PermissionDenied(msg)
