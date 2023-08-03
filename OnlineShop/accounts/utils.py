from kavenegar import *
from OnlineShop.settings import API_KEY_KAVENEGAR
import jwt
import datetime
from django.conf import settings


def send_otp_code(phone_number, otp_code):

    try:
        api = KavenegarAPI(API_KEY_KAVENEGAR)

        params = {
            "sender": "",  # optional
            "receptor": phone_number,
            "message": f"{otp_code}آنلاین شاپ نورا\nکد تایید شما: ",
        }
        print("*************************************")
        print(params)
        response = api.sms_send(params)
        print("response:", response)
        print("status:", api.sms_status())
        print("*************************************")
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)


def generate_access_token(user, expiration_time_minutes=60):

    access_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=0, minutes=expiration_time_minutes),
        "iat": datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(
        access_token_payload, settings.SECRET_KEY, algorithm="HS256"
    )

    return access_token


def generate_refresh_token(user, expiration_time_days=7):
    refresh_token_payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow()
        + datetime.timedelta(days=expiration_time_days),
        "iat": datetime.datetime.utcnow(),
    }
    refresh_token = jwt.encode(
        refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm="HS256"
    )
    return refresh_token
