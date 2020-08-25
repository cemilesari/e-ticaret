from requests import get as get_request
from .cryptograph import sha1
from django.conf import settings
import pyotp

def is_pwnd_password(password):
    password_hash = sha1(password)
    print('password_hash: ', password_hash.upper())
    print(password_hash[:5])

def check_two_factor_authentication(key, otp):
    p = 0
    try:
        p = int(otp)
    except:
        return False
    t = pyotp.TOTP(key)
    resp = t.verify(otp=p)
    return resp

def create_qr_link(secret, user):
    from main.users.models.user import User

    totp = pyotp.TOTP(secret)
    return totp.provisioning_uri(
        getattr(user, User.USERNAME_FIELD),
        settings.TWO_FACTOR_APPLICATION_ISSUER_NAME,
    )