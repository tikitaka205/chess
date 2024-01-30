from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainSlidingView,
    TokenRefreshSlidingView,
)

from user.views import UserView


urlpatterns = [
    
    # 회원 가입 
    path('', UserView.as_view(), name='user_view'),

    # jwt 토큰
    path('api/token/', TokenObtainSlidingView.as_view(), name='token_obtain'),
    path('api/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('check/', UserView.as_view(), name='user_check'),

]