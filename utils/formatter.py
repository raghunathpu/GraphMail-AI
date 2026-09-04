from jinja2 import Template


def clean_text(text: str) -> str:
    return " ".join(text.split())


def format_email(
    subject: str,
    sender_name: str,
    body: str,
    user_name: str
) -> str:

    cleaned_subject = clean_text(subject)
    cleaned_sender = clean_text(sender_name)
    cleaned_user = clean_text(user_name)

    template = Template(
"""
Subject: Re: {{ subject }}

Hi {{ sender }},

{{ body }}

Best regards,
{{ user }}
"""
    )

    return template.render(
        subject=cleaned_subject,
        sender=cleaned_sender,
        body=body.strip(),
        user=cleaned_user
    )
