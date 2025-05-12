from django.urls import path
from .views import GameStatusView, GameNextRoundView, GameStartView, GameStopView

urlpatterns = [
    path('stats/', GameStatusView.as_view(), name='game-stats'),
    path('next-round/', GameNextRoundView.as_view(), name='game-next-round'),
    path('start/', GameStartView.as_view(), name='game-start'),
    path('stop/', GameStopView.as_view(), name='game-stop'),
]
