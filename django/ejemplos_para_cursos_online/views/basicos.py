from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_area_aula(request):
    try:
        largo = float(request.data.get('largo', 0))
        ancho = float(request.data.get('ancho', 0))
    except (ValueError, TypeError):
        return Response({"error": "Parametros invalidos"}, status=status.HTTP_400_BAD_REQUEST)

    area = largo * ancho
    capacidad_estimada = int(area / 1.5) 
    
    return Response({
        "largo_metros": largo,
        "ancho_metros": ancho,
        "area_total": area,
        "capacidad_estudiantes": capacidad_estimada,
        "recomendacion": f"El aula puede albergar aproximadamente {capacidad_estimada} estudiantes"
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def tabla_horarios(request):
    try:
        curso_id = int(request.query_params.get('curso_id', 1))
        horas_por_dia = int(request.query_params.get('horas_por_dia', 2))
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    
    dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
    horarios = []
    
    for i, dia in enumerate(dias, 1):
        hora_inicio = 8 + (i * horas_por_dia)
        hora_fin = hora_inicio + horas_por_dia
        horarios.append(f"{dia}: {hora_inicio}:00 - {hora_fin}:00")
    
    return Response({
        "curso_id": curso_id,
        "horas_por_dia": horas_por_dia,
        "horarios_semanales": horarios,
        "total_horas_semana": len(dias) * horas_por_dia
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def contar_estudiantes_aprobados(request):
    try:
        calificaciones = request.data.get('calificaciones', [])
        nota_minima = request.data.get('nota_minima', 60)
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"},
                         status=status.HTTP_400_BAD_REQUEST)
    try:
        nota_minima = float(nota_minima)
        lista_calificaciones = [float(n) for n in calificaciones]
    except (TypeError, ValueError):
        return Response({"error": "Valores numericos invalidos"},
                         status=status.HTTP_400_BAD_REQUEST)
    
    aprobados = 0
    reprobados = 0
    
    for calificacion in lista_calificaciones:
        if calificacion >= nota_minima:
            aprobados += 1
        else:
            reprobados += 1
    
    porcentaje_aprobacion = (aprobados / len(lista_calificaciones)) * 100 if lista_calificaciones else 0
    
    return Response({
        "calificaciones": lista_calificaciones,
        "nota_minima": nota_minima,
        "estudiantes_aprobados": aprobados,
        "estudiantes_reprobados": reprobados,
        "total_estudiantes": len(lista_calificaciones),
        "porcentaje_aprobacion": round(porcentaje_aprobacion, 2),
        "estado_curso": "Exitoso" if porcentaje_aprobacion >= 70 else "Necesita mejoras"
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_duracion_curso(request):
    try:
        modulos = request.data.get('modulos', 1)
        lecciones_por_modulo = request.data.get('lecciones_por_modulo', 1)
        minutos_por_leccion = request.data.get('minutos_por_leccion', 30)
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        modulos = int(modulos)
        lecciones_por_modulo = int(lecciones_por_modulo)
        minutos_por_leccion = int(minutos_por_leccion)
    except (TypeError, ValueError):
        return Response({"error": "Los valores deben ser numeros enteros"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if modulos <= 0 or lecciones_por_modulo <= 0 or minutos_por_leccion <= 0:
        return Response({"error": "Todos los valores deben ser positivos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    total_lecciones = modulos * lecciones_por_modulo
    total_minutos = total_lecciones * minutos_por_leccion
    total_horas = total_minutos / 60
    
    return Response({
        "modulos": modulos,
        "lecciones_por_modulo": lecciones_por_modulo,
        "minutos_por_leccion": minutos_por_leccion,
        "total_lecciones": total_lecciones,
        "duracion_minutos": total_minutos,
        "duracion_horas": round(total_horas, 2),
        "tiempo_estimado": f"{int(total_horas)} horas y {total_minutos % 60} minutos"
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def promedio_calificaciones_curso(request):
    try:
        calificaciones = request.data.get('calificaciones', [])
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if not isinstance(calificaciones, list):
        return Response({"error": "Debe enviar una lista de calificaciones"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if len(calificaciones) == 0:
        return Response({"error": "La lista de calificaciones no puede estar vacia"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lista_calificaciones = [float(n) for n in calificaciones]
    except (TypeError, ValueError):
        return Response({"error": "Todas las calificaciones deben ser numeros validos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    suma_total = sum(lista_calificaciones)
    cantidad = len(lista_calificaciones)
    promedio = suma_total / cantidad
    
    # Determinar nivel de rendimiento
    if promedio >= 90:
        rendimiento = "Excelente"
    elif promedio >= 80:
        rendimiento = "Muy Bueno"
    elif promedio >= 70:
        rendimiento = "Bueno"
    elif promedio >= 60:
        rendimiento = "Regular"
    else:
        rendimiento = "Deficiente"
    
    return Response({
        "calificaciones": lista_calificaciones,
        "cantidad_estudiantes": cantidad,
        "suma_total": suma_total,
        "promedio_curso": round(promedio, 2),
        "nivel_rendimiento": rendimiento,
        "resumen": f"El curso tiene un promedio de {round(promedio, 2)} con {cantidad} estudiantes - Rendimiento: {rendimiento}"
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_progreso_estudiante(request):
    try:
        lecciones_completadas = request.data.get('lecciones_completadas', 0)
        total_lecciones = request.data.get('total_lecciones', 1)
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        lecciones_completadas = int(lecciones_completadas)
        total_lecciones = int(total_lecciones)
    except (TypeError, ValueError):
        return Response({"error": "Los valores deben ser numeros enteros"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if total_lecciones <= 0:
        return Response({"error": "El total de lecciones debe ser mayor a cero"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if lecciones_completadas < 0:
        return Response({"error": "Las lecciones completadas no pueden ser negativas"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    if lecciones_completadas > total_lecciones:
        return Response({"error": "Las lecciones completadas no pueden ser mayores al total"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    porcentaje_progreso = (lecciones_completadas / total_lecciones) * 100
    lecciones_restantes = total_lecciones - lecciones_completadas
    
    # Determinar estado
    if porcentaje_progreso == 100:
        estado = "Curso Completado"
    elif porcentaje_progreso >= 75:
        estado = "Casi Terminando"
    elif porcentaje_progreso >= 50:
        estado = "En Buen Progreso"
    elif porcentaje_progreso >= 25:
        estado = "Iniciando"
    else:
        estado = "Recien Comenzando"
    
    return Response({
        "lecciones_completadas": lecciones_completadas,
        "total_lecciones": total_lecciones,
        "lecciones_restantes": lecciones_restantes,
        "porcentaje_progreso": round(porcentaje_progreso, 2),
        "estado_progreso": estado,
        "mensaje_motivacional": f"Has completado {lecciones_completadas} de {total_lecciones} lecciones. !{estado}!"
    })