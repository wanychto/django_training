from django.urls import path
from . import views
from .views import AttributeCreateView, AttributeListView, AttributeUpdateView, AttributeDeleteView, SparePartTypeCreateView, SparePartTypeUpdateView, SparePartTypeListView, SparePartTypeDeleteView, SparePartCreateView, SparePartDetailView, SparePartUpdateView, SparePartListView, SparePartDeleteView
app_name= 'spare_parts'

urlpatterns = [
    path('attributes/create/', AttributeCreateView.as_view(), name='attribute_create'),
    path('attributes/', AttributeListView.as_view(), name='attribute_list'),
    path('attributes/<int:pk>/', AttributeUpdateView.as_view(), name='attribute_update'),
    path('attributes/<int:pk>/delete/', AttributeDeleteView.as_view(), name='attribute_delete'),
    path('sparepart-types/create/', SparePartTypeCreateView.as_view(), name='spareparttype_create'),
    path('sparepart-types/<int:pk>/', SparePartTypeUpdateView.as_view(), name='spareparttype_update'),
    path('sparepart-types/', SparePartTypeListView.as_view(), name='spareparttype_list'),
    path('sparepart-types/<str:name>/delete/', SparePartTypeDeleteView.as_view(), name='spareparttype_delete'),
    path('create/', SparePartCreateView.as_view(), name='sparepart_create'),
    path('<int:pk>/', SparePartDetailView.as_view(), name='sparepart_detail'),
    path('<int:pk>/edit/', SparePartUpdateView.as_view(), name='sparepart_update'),
    path('', SparePartListView.as_view(), name='sparepart_list'),
    path('<int:pk>/delete/', SparePartDeleteView.as_view(), name='sparepart_delete'),
]
