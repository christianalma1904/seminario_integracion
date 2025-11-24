from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models.categoria_curso import CategoriaCurso
from ..serializers.categoria_curso import CategoriaCursoSerializer

class CategoriaCursoViewSet(viewsets.ModelViewSet):
    queryset = CategoriaCurso.objects.all()
    serializer_class = CategoriaCursoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['activa']
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'fecha_creacion']
    ordering = ['nombre']

    @action(detail=True, methods=['get'])
    def cursos(self, request, pk=None):
        categoria = self.get_object()
        cursos = categoria.cursos.filter(activo=True)
        from ..serializers.curso import CursoBasicoSerializer
        serializer = CursoBasicoSerializer(cursos, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def con_cursos(self, request):
        categorias = CategoriaCurso.objects.filter(
            activa=True,
            cursos__activo=True
        ).distinct()
        serializer = self.get_serializer(categorias, many=True)
        return Response(serializer.data)