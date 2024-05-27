import hashlib
import secrets
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from decouple import config

DEPLOY = config('DJANGO_DEPLOY', default=False, cast=bool)

class HashMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if not request.COOKIES.get('auth_hash'):
            user_ip = request.META.get('REMOTE_ADDR', '')
            user_agent = request.META.get('HTTP_USER_AGENT', '')
            hash_source = user_ip + user_agent + secrets.token_hex(16)
            auth_hash = hashlib.sha256(hash_source.encode()).hexdigest()
            response.set_cookie('auth_hash', auth_hash, max_age=7*24*60*60, secure=DEPLOY, httponly=True)
        return response
