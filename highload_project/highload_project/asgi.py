import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from file_processor.consumers import ProgressConsumer  # Import the consumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'highload_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            [
                path('ws/progress/', ProgressConsumer.as_asgi()),  # WebSocket route
            ]
        )
    ),
})
