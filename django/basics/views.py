from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([AllowAny])
def area_triangulo(request):
    try:
        base= float(request.data.get('base', 0))
        altura= float(request.data.get('altura', 0))
    except (ValueError, TypeError):
        return Response({"error": "Parametros invalidos"}, status=status.HTTP_400_BAD_REQUEST)

    area = (base * altura) / 2
    return Response({
        "base": base,
        "altura": altura,
        "area": area
    })

@api_view(['GET'])
@permission_classes([AllowAny])
def tabla_multiplicar(request):
    try:
        n = int(request.query_params.get('numero', 0))
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, status=status.HTTP_400_BAD_REQUEST)
    tabla = [f"{n}x{i}={n*i}" for i in range(1, 11)]
    return Response({
        "numero": n,
        "tabla": tabla,
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def contar_mayores(request):
    try:
        numeros= request.data.get('numeros',[])
        limite = request.data.get('limite',0)
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"},
                         status=status.HTTP_400_BAD_REQUEST)
    try:
        limite = float(limite)
        lista_numeros = [float(n) for n in numeros]
    except (TypeError, ValueError):
        return Response({"error": "valores numericos invalidos"},
                         status=status.HTTP_400_BAD_REQUEST)
    contador=0
    for n in lista_numeros:
        if n>limite:
            contador +=1
    return Response({
        "numeros": lista_numeros,
        "limite": limite,
        "mayores": contador
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def sumar_consecutivos(request):
    try:
        limite = request.data.get('limite', 0)
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, 
                       status=status.HTTP_400_BAD_REQUEST)

    
    resultado = 0
    i = 1
    
    while i <= limite:
        resultado += i
        i += 1
    return Response({
        "limite": limite,
        "suma_total": resultado
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def calcular_promedio(request):

    try:
        numeros = request.data.get('numeros', [])
    except (TypeError, ValueError):
        return Response({"error": "Parametros invalidos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Convertir todos los elementos a números
        lista_numeros = [float(n) for n in numeros]
    except (TypeError, ValueError):
        return Response({"error": " valores validos"}, 
                       status=status.HTTP_400_BAD_REQUEST)
    
    suma_total = sum(lista_numeros)
    cantidad = len(lista_numeros)
    promedio = suma_total / cantidad
    
    return Response({
        "numeros": lista_numeros,
        "promedio": round(promedio, 2)    
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def potencia(request):
    try:
        base = float(request.data.get('base', 0))
        exponente = float(request.data.get('exponente', 0))
    except (ValueError, TypeError):
        return Response({"error": "Parametros invalidos"}, status=status.HTTP_400_BAD_REQUEST)

    resultado = base ** exponente
    return Response({
        "base": base,
        "exponente": exponente,
        "resultado": resultado
    })