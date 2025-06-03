from django.urls import path
from .views import ConflictListView, CommodityListView, ConflictDetailView, CommodityDetailView
urlpatterns = [
    path('conflicts/', ConflictListView.as_view(), name='conflict-list'),
    path('conflicts/<int:pk>/', ConflictDetailView.as_view(), name='conflict-detail'),
    path('commodities/', CommodityListView.as_view(), name='commodity-list'),
    path('commodities/<int:pk>/', CommodityDetailView.as_view(), name='commodity-detail'),
]