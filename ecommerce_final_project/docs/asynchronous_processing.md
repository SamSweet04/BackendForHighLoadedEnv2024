# Asynchronous Processing with Celery

This document provides details on the Celery tasks I implemented in `tasks.py` for asynchronous processing in my project. It includes an explanation of the tasks and example usage for sending order confirmation emails and processing payments.

---

## Prerequisites

To use Celery tasks in this project, I set up the following:

1. **Install Required Dependencies**:
   ```bash
   pip install celery[redis] django-celery-results
   ```
2. **Start Redis Server (used as the Celery broker)**:
   ```bash
   redis-server
   ```
3. **Start Celery Worker**:
   ```bash
   celery -A ecommerce_final_project worker --loglevel=info
   ```
   
4. **Configured email settings in settings.py to enable sending emails.**

## Tasks Defined in tasks.py

1. **send_order_confirmation_email**

I created this task to send order confirmation emails asynchronously. It ensures that the main thread is not blocked during email sending.
```python
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
```

2. **process_payment**

This task simulates payment processing for orders asynchronously. It can be expanded to integrate with a payment gateway in the future.

```python

@shared_task
def process_payment(order_id):
    """
    Симуляция обработки платежа. Email не передаётся, используется только order_id.
    """
    try:
        return f"Платеж для заказа #{order_id} успешно обработан."
    except Exception as e:
        return f"Ошибка обработки платежа для заказа #{order_id}: {str(e)}"
```

### Example Usage

### Sending Order Confirmation Email

To send an order confirmation email asynchronously, I used the following method:

```python
from .tasks import send_order_confirmation_email

send_order_confirmation_email.delay(order_id=123, customer_email="customer@example.com")
```

### Processing Payment

To process payments for an order asynchronously, I implemented the following:

```python 
from .tasks import process_payment

process_payment.delay(order_id=123)
```

### Example API Integration

1. **API Endpoint: Create an Order**

I integrated the Celery tasks with my API to trigger them during order creation.

	•	Endpoint: /api/create-order/
	•	HTTP Method: POST
	•	Request Body:

```json
{
    "orderId": "123",
    "userId": 1,
    "totalAmount": 150.00,
    "customerEmail": "customer@example.com"
}
```

### Response:
```json
{
    "message": "Order #123 created. Email sent to customer@example.com.",
    "data": {
        "message": "Order created successfully!"
    }
}
```
### Workflow:

	•	The send_order_confirmation_email task sends the email asynchronously.
	•	The process_payment task handles payment processing asynchronously.

### Troubleshooting

1. Celery Worker Not Running

	•	I ensured Redis was running and that I started the Celery worker using the correct command.

2. Email Not Sent

	•	I verified the email backend configuration in settings.py.

	•	Checked for errors in the Celery worker logs to ensure tasks were being executed.

3. Payment Task Not Triggered

	•	I double-checked that process_payment.delay() was being called properly in the relevant API view.

**This implementation has improved the performance of my project by offloading email sending and payment processing to Celery tasks. It ensures that the main application remains responsive even under load.**