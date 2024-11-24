from django.db import models
from django.core.exceptions import ValidationError
from encrypted_model_fields.fields import EncryptedTextField

class Email(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = EncryptedTextField()  # Поле с шифрованием
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Custom validation logic
        if not self.subject or len(self.subject.strip()) < 3:
            raise ValidationError("Subject must be at least 3 characters long.")
        if not self.body or len(self.body.strip()) < 10:
            raise ValidationError("Body must be at least 10 characters long.")
