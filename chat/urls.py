from django.urls import path
from chat.views import ChatView
# from . import views


urlpatterns = [
    # path("", views.index, name="index"),
    # path("<str:room_name>/", views.room, name="room"),
    path('', ChatView.as_view(), name='index'),
    path('<str:room_name>/', ChatView.as_view(), name='room'),

]