from core.celery import app
from django.core.mail import send_mail

import os
import requests



@app.task
def send_mail_task(email, html_message):
    #send_mail(
    #   subject=subject,
    #   message = message,
    #   from_email = f"Animal Farm NG <hello@animalfarm.ng>",
    #   recipient_list = recipient_list,
    #   fail_silently=True,
    #   html_message=html_message
    #)

    requests.post("https://api.mailgun.net/v3/animalfarm.ng/messages", auth=("api", os.environ.get("MAILGUN_API_KEY")), data={"from": "Animal Farm NG <hello@animalfarm.ng>", "to": [email],  "subject": "Verify Your Account", "text": html_message})