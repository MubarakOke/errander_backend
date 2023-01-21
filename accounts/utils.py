from django.core.mail import send_mail
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import get_template


def encode_user_id(id):
    uuid_encoded= urlsafe_base64_encode(smart_bytes(id))   
    return uuid_encoded

def decode_user_id(uuid_encoded):
    try:
        uuid_decoded= force_str(urlsafe_base64_decode(uuid_encoded))
        return uuid_decoded
    except:
        return None

def password_reset_token_is_valid(user, token):
    if PasswordResetTokenGenerator().check_token(user, token):
        return True
    else:
        return False

def generate_password_reset_url(user, request, user_type, server):
    """
    Generate the password reset url
    """
    user_id_encoded= encode_user_id(user.id)
    token= PasswordResetTokenGenerator().make_token(user)

    current_site= get_current_site(request).domain
    domain= current_site.split(":")
    if user_type == "customer" and server== "development":
        base_url= "localhost:3000"
    elif user_type == "customer" and server== "production":
        base_url= ""
    elif user_type == "errander" and server== "development":
        base_url= "localhost:3001" 
    elif user_type == "errander" and server== "production":
        base_url= "" 
    else:
        base_url= ""
    
    relative_link= f"change-forget-password/{str(token)}/{user_id_encoded}"
    absolute_url= f"http://{base_url}/{relative_link}"

    return absolute_url

def send_password_reset_email(user, request, user_type, server):
    """
    Send password reset email to the recipient.

    """
    user_name = user.fullname
    absolute_url= generate_password_reset_url(user, request, user_type, server)
    subject = "Reset your account password"
    email_body= f"""
    Use the link below to reset your password.
    {absolute_url}
    """
    context = {"user_name": user_name, "absolute_url": absolute_url}
    try:
        send_mail(
                subject=subject,
                message=email_body,
                from_email=None,
                html_message=get_template("accounts/password_reset.html").render(context),
                recipient_list=[user.email],
                fail_silently=False,
                )
        return True
    except Exception as exception:
        return False