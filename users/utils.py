from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from .token import account_activation_token
from django.core.mail import EmailMessage
from users.models import User
from django.http import HttpResponse
from lms import settings
from smtplib import SMTPAuthenticationError
import ssl

def activateEmail(request, user, to_email):
    html_template="users/email_verification.html"
    html_message=render_to_string(html_template,{
        'user': user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        })
    subject="Verify your email"
    email_from=settings.EMAIL_HOST_USER
    reciepent_list=[to_email]
    message=EmailMessage(subject, html_message, from_email=email_from, to=reciepent_list)
    message.content_subtype='html'

    try: 
        if message.send():
            return HttpResponse("Please check your account for verification!")
        else:
            return HttpResponse("Invalid details!")
        
    except SMTPAuthenticationError:
        # Handling SMTP Authentication Error specifically
        return "Authentication failed. Please ensure you've paid for this service."
    except ssl.SSLError as e:
        return HttpResponse(f"SSL error occurred: {e}")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except:
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for verification. You can login now.")
        # return redirect('users:index')
    else:
        user.is_active=False
        user.delete()
        return HttpResponse("User not verified.")