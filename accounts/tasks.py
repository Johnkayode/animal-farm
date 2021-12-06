from core.celery import app
from django.core.mail import send_mail



@app.task
def send_mail_task(subject, message, recipient_list, html_message):
    send_mail(
        subject=subject,
        message = message,
        from_email = f"Animal Farm NG <hello@animalfarm.ng>",
        recipient_list = recipient_list,
        fail_silently=True,
        html_message=html_message
    )