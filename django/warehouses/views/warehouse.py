from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from ..models import Warehouse
from ..serializers import WarehouseSerializer

@api_view(["GET"])
def warehouse_get_list(request):
    qs = Warehouse.objects.all()
    q = (request.query_params.get("q") or "").strip()
    if q:
        qs = qs.filter(Q(code__icontains=q) |
                       Q(name__icontains=q) |
                       Q(city__icontains=q))
    data = WarehouseSerializer(qs, many=True).data
    return Response(data, status=status.HTTP_200_OK)

@api_view(["POST"])
def warehouse_create(request):
    serializer = WarehouseSerializer(data=request.data)
    if serializer.is_valid():
        warehouse = serializer.save()
        return Response(WarehouseSerializer(warehouse).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def warehouse_get_by_id(request, warehouse_id: int):
    try:
        warehouse = Warehouse.objects.get(pk=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response(
            {'Detail': 'Not found'},
            status=status.HTTP_404_NOT_FOUND)
    return Response(WarehouseSerializer(warehouse).data, status=status.HTTP_200_OK)

@api_view(["PUT"])
def warehouse_update(request, warehouse_id: int):
    try:
        warehouse = Warehouse.objects.get(pk=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response(
            {'Detail': 'Not found'},
            status=status.HTTP_404_NOT_FOUND)
    serializer = WarehouseSerializer(warehouse, data=request.data)
    if serializer.is_valid():
        warehouse = serializer.save()
        return Response(WarehouseSerializer(warehouse).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
def warehouses_delete(request, warehouse_id: int):
    try:
        warehouse = Warehouse.objects.get(pk=warehouse_id)
    except Warehouse.DoesNotExist:
        return Response({'Detail': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
    warehouse.delete()
    return Response({'Detail': 'Registro eliminado'}, status=status.HTTP_200_OK)
