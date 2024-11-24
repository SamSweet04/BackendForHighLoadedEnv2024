from celery import shared_task
import csv
from .models import UploadedFile


@shared_task(bind=True)
def process_csv_file(self, file_id):
    try:
        uploaded_file = UploadedFile.objects.get(id=file_id)
        uploaded_file.status = 'Processing'
        uploaded_file.save()

        # Process CSV
        with uploaded_file.file.open('r') as f:
            reader = csv.reader(f)
            for row in reader:
                pass

        uploaded_file.status = 'Completed'
        uploaded_file.save()
    except Exception as e:
        uploaded_file.status = 'Error'
        uploaded_file.save()
        raise self.retry(exc=e, countdown=60, max_retries=3)
