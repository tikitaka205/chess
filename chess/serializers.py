from chess.models import ChessLog
from rest_framework import serializers


class GameInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChessLog
        fields = '__all__'

class ChessMoveSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChessLog
        fields = '__all__'
