from django.urls import path
from .views import AuthenticateView

app_name= 'accounts'

urlpatterns = [
    path('auth/', AuthenticateView.as_view(), name='auth'),
]