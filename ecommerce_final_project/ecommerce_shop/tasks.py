from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_order_confirmation_email(order_id, customer_email):
    """
    Отправляет email с подтверждением заказа. Email передаётся в функцию напрямую.
    """
    try:
        subject = f"Подтверждение заказа #{order_id}"
        message = f"Спасибо за ваш заказ #{order_id}! Мы приступили к его обработке."
        send_mail(
            subject,
            message,
            'saule.arystanbek.2004@mail.ru',  # Отправитель
            [customer_email],  # Получатель
        )
        return f"Email для заказа #{order_id} успешно отправлен на {customer_email}."
    except Exception as e:
        return f"Ошибка отправки email для заказа #{order_id}: {str(e)}"


@shared_task
def process_payment(order_id):
    """
    Симуляция обработки платежа. Email не передаётся, используется только order_id.
    """
    try:
        return f"Платеж для заказа #{order_id} успешно обработан."
    except Exception as e:
        return f"Ошибка обработки платежа для заказа #{order_id}: {str(e)}"