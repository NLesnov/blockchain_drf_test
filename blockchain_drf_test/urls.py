from django.urls import path, include

urlpatterns = [
    path('tokens/', include('tokens.urls'))
]
