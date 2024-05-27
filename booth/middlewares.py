from django.utils.deprecation import MiddlewareMixin
from django.core import signing
import secrets

# 사용자가 조작할 수 없는 서명된 토큰을 쿠키에 저장
# 진짜 조작이 안되는지는 모르겠음...
class ClientTokenMiddleware(MiddlewareMixin):
    def process_request(self, request):
        client_token = request.COOKIES.get('client_token')
        if client_token:
            try:
                token = signing.loads(client_token)
                request.META['client_token'] = token
            except signing.BadSignature:
                request.META['client_token'] = None
        else:
            request.META['client_token'] = None

    def process_response(self, request, response):
        if 'client_token' not in request.META or not request.META['client_token']:
            token = secrets.token_hex(16)
            signed_token = signing.dumps(token)
            response.set_cookie('client_token', signed_token, max_age=365*24*60*60, httponly=True)
            request.META['client_token'] = token
        return response