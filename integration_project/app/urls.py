from django.urls import path
from .views import CorrelationView

app_name = 'app'

urlpatterns = [
    path('', CorrelationView.as_view(), name='commodities'),
]