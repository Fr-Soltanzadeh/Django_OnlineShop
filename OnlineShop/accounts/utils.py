from kavenegar import *
from OnlineShop.settings import API_KEY_KAVENEGAR


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
