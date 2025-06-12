import os
from django.core.asgi import get_asgi_application
import sys

# Указываем настройки напрямую
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gis.settings')

# Инициализируем приложение
django_asgi_app = get_asgi_application()

# Добавляем путь к проекту в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_application():
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    from game.routing import websocket_urlpatterns  # Ленивый импорт

    application = ProtocolTypeRouter({
        "http": django_asgi_app,
        "websocket": AuthMiddlewareStack(
            URLRouter(
                websocket_urlpatterns
            )
        ),
    })
    return application

application = get_application()