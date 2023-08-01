import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import exceptions
from rest_framework.response import Response
from .utils import generate_access_token, generate_refresh_token
from rest_framework.views import APIView
import random
from .serializers import LoginSerializer, OtpCodeSerializer
from .utils import send_otp_code
from .models import User, OtpCode, CustomerProfile
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from cart.utils import add_session_to_user_cart
from rest_framework import views, permissions, status


User = get_user_model()


class LoginOrRegisterApiView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        
        serializer= LoginSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            otp_code = random.randint(1000, 9999)
            send_otp_code(phone_number, otp_code)
            if  OtpCode.objects.filter(phone_number=phone_number).exists():
                OtpCode.objects.get(phone_number=phone_number).delete()
            OtpCode.objects.create(phone_number=phone_number, code=otp_code)
            request.session["login_info"] = {
                "phone_number": phone_number,
                "redirect_to": serializer.data.get("next"),
            }
            request.session.save()
            messages.success(
                request,
                f"A verification code has been sent to your phone number",
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeApiView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer= OtpCodeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_number = request.session["login_info"]["phone_number"]
            otp_code = OtpCode.objects.get(phone_number=phone_number)
            if serializer.data["verify_code"] == str(otp_code.code):
                if not User.objects.filter(phone_number=phone_number).exists():
                    user = User.objects.create(phone_number=phone_number)
                else:
                    user = User.objects.get(phone_number=phone_number)
                redirect_to = request.session["login_info"]["redirect_to"]
                login(request, user)
                add_session_to_user_cart(request)
                otp_code.delete()
                request.session["login_info"]={}
                request.session.save()
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                messages.success(request, "You have successfully logged in.")
                return Response(data={"redirect_to":redirect_to, 'token': access_token, 'refresh_token':refresh_token}, status=status.HTTP_200_OK)
                
        messages.error(
            request,
            "The entered code is not correct. Try again",
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenApiView(APIView):
    '''
    To obtain a new access_token this view expects 2 important things:
        1. a cookie that contains a valid refresh_token
        2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
    '''
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refreshtoken')
        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Authentication credentials were not provided.')
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('user is inactive')

        access_token = generate_access_token(user)
        return Response({'access_token': access_token})

