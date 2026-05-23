import sib_api_v3_sdk
import os
from django.conf import settings
from django.template.loader import render_to_string

def send_verification_email(email, code):
    if not settings.BREVO_API_KEY:
        raise ValueError("BREVO_API_KEY is not configured")

    BREVO = os.getenv("BREVO_API_KEY")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = BREVO

    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(
        sib_api_v3_sdk.ApiClient(configuration)
    )

    html = render_to_string("email_verify.html", {"code": code})

    email_data = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={
            "email": settings.DEFAULT_FROM_EMAIL,
            "name": "Voting System"
        },
        subject="Verify Email",
        html_content=html,
    )

    api_instance.send_transac_email(email_data)