#!/bin/bash

echo "Pulling latest changes..."
git pull origin main

echo "Installing dependencies..."
source /path/to/venv/bin/activate
pip install -r requirements.txt

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Restarting server..."

echo "Stopping Gunicorn..."
pkill -f gunicorn

echo "Starting Gunicorn..."
gunicorn ecommerce_final_project.wsgi:application \
    --bind 127.0.0.1:8000 \
    --workers 3 &

echo "Restarting Nginx with Homebrew..."
brew services restart nginx

echo "Deployment complete!"