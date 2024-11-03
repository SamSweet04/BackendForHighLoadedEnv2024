from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Order
import logging


logger = logging.getLogger(__name__)

@shared_task
def process_order(order_id):
    try:
        # Retrieve the order by ID
        order = Order.objects.get(id=order_id)

        # Prepare email details
        subject = f"Order Confirmation for Order #{order.id}"
        body = (
            f"Hello {order.user.username},\n\n"
            f"Thank you for your purchase!\n"
            f"Here are your order details:\n"
            f"Product: {order.product.name}\n"
            f"Quantity: {order.quantity}\n"
            f"Total Price: ${order.total_price}\n\n"
            f"We appreciate your business!"
        )
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [order.user.email]

        # Send email using the send_mail function
        send_mail(
            subject,
            body,
            from_email,
            recipient_list,
            fail_silently=False,  # Raise exceptions if the email fails to send
        )

        logger.info(f"Order #{order.id} processed and email sent to {order.user.email}")

    except Order.DoesNotExist:
        logger.error(f"Order with ID {order_id} does not exist.")
    except Exception as e:
        logger.error(f"An error occurred while processing order {order_id}: {str(e)}")
