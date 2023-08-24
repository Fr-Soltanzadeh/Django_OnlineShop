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
from accounts.models import User, OtpCode, CustomerProfile, Address
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from cart.utils import add_session_to_user_cart
from rest_framework import views, permissions, status
from .serializers import CustomerSerializer, AddressSerializer 
from .serializers import CustomerAbstractSerializer, CustomerProfileSerializer
from rest_framework import generics
from rest_framework import mixins
from accounts.permissions import IsOwnerOrReadOnly
import logging


User = get_user_model()
logger=logging.getLogger('online_shop')


class LoginOrRegisterApiView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, *args, **kwargs):

        serializer = LoginSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            phone_number = serializer.data["phone_number"]
            otp_code = random.randint(1000, 9999)
            send_otp_code(phone_number, otp_code)
            if OtpCode.objects.filter(phone_number=phone_number).exists():
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
    authentication_classes = []

    def post(self, request):
        serializer = OtpCodeSerializer(data=request.data)
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
                logger.info(f"User with phone_number:{user.phone_number} signed in.")
                add_session_to_user_cart(request)
                access_token = generate_access_token(user)
                refresh_token = generate_refresh_token(user)
                otp_code.delete()
                request.session["login_info"] = {}
                request.session.save()
                messages.success(request, "You have successfully logged in.")
                return Response(
                    data={
                        "redirect_to": redirect_to,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    status=status.HTTP_200_OK,
                )

        messages.error(
            request,
            "The entered code is not correct. Try again",
        )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenApiView(APIView):

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        refresh_token = request.headers.get("Authorization")
        if refresh_token is None or refresh_token == "Bearer null":
            return Response({"message": "invalid token"}, status.HTTP_401_UNAUTHORIZED)
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided."
            )
        refresh_token = refresh_token.replace("Bearer", "").replace(" ", "")
        try:
            payload = jwt.decode(
                refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                "expired refresh token, please login again."
            )
        except:
            raise exceptions.AuthenticationFailed(
                "Couldn't parse token, please login again."
            )

        user = User.objects.filter(id=payload.get("user_id")).first()
        if user is None:
            raise exceptions.AuthenticationFailed("User not found")

        if not user.is_active:
            raise exceptions.AuthenticationFailed("user is inactive")

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response(
            {"access_token": access_token, "refresh_token": refresh_token},
            status=status.HTTP_200_OK,
        )


class CustomerApiView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, format=None):
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CustomerAbstractAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        serializer = CustomerAbstractSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        serializer = CustomerAbstractSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"m":"done"})

class CustomerProfileAPIView(APIView):

    permission_classes = [IsOwnerOrReadOnly]
    def get(self, request, format=None):
        customer_profile = CustomerProfile.objects.get_or_create(customer=self.request.user)
        serializer = CustomerProfileSerializer(customer_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CustomerProfileSerializer(data=request.data)
        if serializer.is_valid():
            CustomerProfile.objects.update_or_create(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerAddressListCreateAPIView(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get(self, request, format=None):
        addresses = Address.objects.filter(user=request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        data = request.data.copy()
        if not data.get("user"):
            data["user"] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAddressDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AddressSerializer
    permission_classes = [IsOwnerOrReadOnly]
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
