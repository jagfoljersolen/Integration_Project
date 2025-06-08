from django.urls import path
from .views import CorrelationView
from . import views

app_name = 'app'

urlpatterns = [

    path('', views.main_dashboard, name='main_dashboard'),
    path('api/dashboard/commodity/', views.dashboard_commodity_api, name='dashboard_commodity_api'),
    path('api/dashboard/conflict/', views.dashboard_conflict_api, name='dashboard_conflict_api'),

    path('correlations/', CorrelationView.as_view(), name='correlations'),
    path('commodities/', views.commodity_dashboard, name='commodities'),
    path('api/commodity-data/', views.commodity_data_api, name='commodity_data_api'),
    path('conflicts/', views.conflict_dashboard, name='conflicts'),
    path('api/conflict-data/', views.conflict_data_api, name='conflict_data_api'),
    path('conflicts_vs_commodities/', views.conflicts_vs_commodities, name='conflicts_vs_commodities'),

    #path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),

]

