# Dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh


COPY . /app/

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
