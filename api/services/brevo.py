import sib_api_v3_sdk
from django.conf import settings
from django.template.loader import render_to_string
from sib_api_v3_sdk.rest import ApiException


def send_verification_email(email, code):
    brevo_api_key = (settings.BREVO_API_KEY or "").strip()

    if not brevo_api_key:
        raise ValueError("BREVO_API_KEY is not configured")

    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key["api-key"] = brevo_api_key

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

    try:
        api_instance.send_transac_email(email_data)
    except ApiException as exc:
        if exc.status == 401:
            raise ValueError(
                "Brevo API key is unauthorized. Generate a new Brevo SMTP/API key "
                "and update BREVO_API_KEY in .env."
            ) from exc
        raise
