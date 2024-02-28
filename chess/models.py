from django.db import models
from user.models import User


#체스 방을 만드는 이유
#턴
#시간제한
#채팅
#
class ChessLog(models.Model):
    class Meta:
        db_table = 'ChessLog'
        ordering = ['-created_at']

    player_1 = models.ForeignKey(User, on_delete = models.CASCADE, related_name='player_1',null=True, blank=True)
    player_2 = models.ForeignKey(User, on_delete = models.CASCADE, related_name='player_2',null=True, blank=True)
    game_state = models.CharField(max_length=100,null=True, blank=True)
    board_state = models.CharField(max_length=100,null=True, blank=True)
    turn = models.BooleanField(default=True,null=True, blank=True)
    move_log = models.CharField(max_length=200,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
