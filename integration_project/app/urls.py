from django.urls import path
from .views import CorrelationView
from . import views

app_name = 'app'

urlpatterns = [
    path('correlations/', CorrelationView.as_view(), name='correlations'),
    path('commodities/', views.commodity_dashboard, name='commodities'),
    path('api/commodity-data/', views.commodity_data_api, name='commodity_data_api'),
    path('conflicts/', views.conflict_dashboard, name='conflicts'),
    path('api/conflict-data/', views.conflict_data_api, name='conflict_data_api'),
    path('conflicts_vs_commodities/', views.conflicts_vs_commodities, name='conflicts_vs_commodities'),
]

