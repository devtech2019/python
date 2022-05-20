from django.core.mail import send_mail

def sendMail(subject, message, recipient):
    send_mail(
        subject=subject,
        message=message,
        from_email='yallacashdubai@gmail.com',
        recipient_list=recipient
    )
    return None
