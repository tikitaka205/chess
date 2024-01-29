from django.urls import path
from chess.views import ChessView

urlpatterns = [
    
    path('', ChessView.as_view(), name='chess_view'),

]