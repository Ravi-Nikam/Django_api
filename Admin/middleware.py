import jwt
from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect,HttpResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed

class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("middleware")
        print(request.path)
        if not request.path.startswith('/login'):  # Exclude login URL
            token = request.COOKIES.get('jwt_token')
            print("tokennnnnnn",token)
            if token:
                try:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                    print(payload,"payload")
                    request.user = payload
                except jwt.ExpiredSignatureError:
                    redirect_url = reverse('login') + '?msg=Token Expire'
                    return redirect(redirect_url)
                    return render(request,'login.html',{"msg":'Token Expire'})
                    raise AuthenticationFailed('Token has expired')
                except jwt.InvalidTokenError:
                    raise AuthenticationFailed('Invalid token')
            else:
                return HttpResponseRedirect('/login')
