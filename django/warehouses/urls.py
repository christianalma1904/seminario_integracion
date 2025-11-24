from django.urls import path
from .views.warehouse import warehouse_get_list, warehouse_create, warehouse_get_by_id, warehouse_update, warehouses_delete

urlpatterns = [
    path('warehouses/', warehouse_get_list, name='warehouse-list'),
    path('warehouses/create/', warehouse_create, name='warehouse-create'),
    path('warehouses/<int:warehouse_id>/', warehouse_get_by_id, name='warehouse-detail'),
    path('warehouses/<int:warehouse_id>/update/', warehouse_update, name='warehouse-update'),
    path('warehouses/<int:warehouse_id>/delete/', warehouses_delete, name='warehouse-delete'),
]