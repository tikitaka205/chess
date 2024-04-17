import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blindchess.settings")

import django
django.setup()
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application

# from chat.routing import websocket_urlpatterns
import chat.routing
django.setup()

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": (
            AuthMiddlewareStack(
                URLRouter(
                    chat.routing.websocket_urlpatterns))
        ),
    }
)

#########################원본
# import os

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# # from channels.security.websocket import AllowedHostsOriginValidator
# from django.core.asgi import get_asgi_application
# import chat.routing
# from chat.routing import websocket_urlpatterns

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blindchess.settings")
# # Initialize Django ASGI application early to ensure the AppRegistry
# # is populated before importing code that may import ORM models.
# django_asgi_app = get_asgi_application()
# application = ProtocolTypeRouter(
#     {
#         "http": django_asgi_app,
#         "websocket": (
#             AuthMiddlewareStack(URLRouter(chat.routing.websocket_urlpatterns))
#         ),
#     }
# )
#########################
# import os
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'egodaeyeo.settings')

# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter

# from django.core.asgi import get_asgi_application
# import chat.routing

# application = ProtocolTypeRouter({
#     'http': get_asgi_application(),
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat.routing.websocket_urlpatterns
#         )
#     )
# })