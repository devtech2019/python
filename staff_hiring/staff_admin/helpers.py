from django.core.mail import send_mail
import math
import random
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
# Function to generate Password
def generatePassword():
    # Declare a digits variable
    # which stored all digits
    digits = "Abcdefgh@#()1234567890"
    Password = ""
    # length of password can be changed
    # by changing value in range
    for i in range(8):
        Password += digits[math.floor(random.random() * 10)]
    return Password

# Function to generate OTP


def generateOTP():
    # Declare a digits variable
    # which stored all digits
    digits = "1234567890"
    Otp = ""
    # length of password can be changed
    # by changing value in range
    for i in range(4):
        Otp += digits[math.floor(random.random() * 10)]
    return (Otp)


# Sending Mail
def sendMail(subject, message, recipient):
    send_mail(
        subject=subject,
        message=message,
        from_email='yallacashdubai@gmail.com',
        recipient_list=recipient
    )
    return None


# def sendMail():
#     send_mail(
#         subject=subject,
#         message=message,
#         from_email='yallacashdubai@gmail.com',
#         recipient_list=recipient
#     )
#     return None


# Html To PDF helper
def html_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
         return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
