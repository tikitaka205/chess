from django.urls import re_path
from . import consumers

# 미들웨어 연결 유저 가져오기위해
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from django.urls import path

# from django.core.wsgi import get_wsgi_application


websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
]

# # 미들웨어 연결 유저 가져오기위해
# # application = ProtocolTypeRouter({
# #     "websocket": AuthMiddlewareStack(
# #         URLRouter([
# #             websocket_urlpatterns
# #         ])
# #     ),
# # })
# application = ProtocolTypeRouter({
#     "http": get_wsgi_application(),  # HTTP 프로토콜 처리
#     "websocket": AuthMiddlewareStack(  # 웹소켓 프로토콜 처리
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })