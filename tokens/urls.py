from django.urls import path
from .views import (
    GetTokenTotalSupplyView,
    CreateTokenView,
    ListTokenView,
)

urlpatterns = [
    path('total_supply/', GetTokenTotalSupplyView.as_view()),
    path('create/', CreateTokenView.as_view()),
    path('list/', ListTokenView.as_view()),
]