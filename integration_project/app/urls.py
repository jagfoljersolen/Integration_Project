from django.urls import path
from .views import CorrelationView
from . import views
from .api_views import ConflictYearlyDataAPI, ConflictListAPI, ConflictIntensityDataApi, ConflictTypesDataApi, CommodityListAPI

app_name = 'app'

urlpatterns = [

    path('', views.main_dashboard, name='main_dashboard'),
    path('api/dashboard/commodity/', views.dashboard_commodity_api, name='dashboard_commodity_api'),
    path('api/dashboard/conflict/', views.dashboard_conflict_api, name='dashboard_conflict_api'),

    path('correlations/', CorrelationView.as_view(), name='correlations'),
    path('api/conflict-data/', ConflictYearlyDataAPI.as_view(), name='conflict_data_api'),
    path('api/conflicts/', ConflictListAPI.as_view(), name='conflict-list-api'),
    path('api/conflict-intensity/', ConflictIntensityDataApi.as_view(), name='conflict-intensity-api'),
    path('api/conflict-types/', ConflictTypesDataApi.as_view(), name='conflict-type-api'),
    path('api/commodities/', CommodityListAPI.as_view(), name='commodity-list'),

    path('commodities/', views.commodity_dashboard, name='commodities'),
    path('conflicts/', views.conflict_dashboard, name='conflicts'),
    path('conflicts_vs_commodities/', views.conflicts_vs_commodities, name='conflicts_vs_commodities'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout')


]

