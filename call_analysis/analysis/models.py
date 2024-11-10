# analysis/models.py
from django.db import models

class CallRecord(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    transcription = models.TextField(null=True, blank=True)
    sentiment = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CallRecord {self.id}"
