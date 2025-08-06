from django.urls import path
from .views import VehicleTypeCreateView, VehicleTypeListView, VehicleTypeUpdateView, VehicleTypeDeleteView, VehicleCreateView, VehicleUpdateView, VehicleDeleteView, VehicleDetailView, VehicleListView


app_name= 'vehicle'

urlpatterns = [
    path('vehicle-types/create/', VehicleTypeCreateView.as_view(), name='vehicletype_create'),
    path('vehicle-types/', VehicleTypeListView.as_view(), name='vehicletype_list'),
    path('vehicle-types/<str:name>/', VehicleTypeUpdateView.as_view(), name='vehicletype_update'),
    path('vehicle-types/<str:name>/delete/', VehicleTypeDeleteView.as_view(), name='vehicletype_delete'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicles_create'),
    path('vehicles/<int:pk>/edit/', VehicleUpdateView.as_view(), name='vehicles_update'),
    path('vehicles/<int:pk>/', VehicleDetailView.as_view(), name='vehicles_detail'),
    path('vehicles/', VehicleListView.as_view(), name='vehicles_list'),
    path('vehicles/<int:pk>/delete/', VehicleDeleteView.as_view(), name='vehicles_delete'),
]
