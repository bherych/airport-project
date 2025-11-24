from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_ticket_email(order, tickets):
    subject = f"Your tickets for order #{order.id}"

    html_message = render_to_string(
        "emails/ticket_email.html",
        {
            "order": order,
            "tickets": tickets,
        },
    )

    plain_message = f"Your tickets for order {order.id}"

    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        html_message=html_message
    )
