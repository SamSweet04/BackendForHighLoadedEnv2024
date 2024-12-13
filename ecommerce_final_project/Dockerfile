# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files
COPY . .

# Expose the port for the Django application
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]FROM ubuntu:latest
LABEL authors="saulearystanbek"

ENTRYPOINT ["top", "-b"]