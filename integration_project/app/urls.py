from django.urls import path
from .views import CorrelationView

app_name = 'app'

urlpatterns = [
    path('correlations/', CorrelationView.as_view(), name='correlations'),
]