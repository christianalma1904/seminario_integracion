from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
import json

class CursosOnlineTestCase(TestCase):
    
    def setUp(self):
        self.client = APIClient()
    
    def test_calcular_area_aula(self):
        data = {
            "largo": 10,
            "ancho": 8
        }
        response = self.client.post('/api/cursos/calcular-area-aula/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['area_total'], 80)
        self.assertEqual(response.data['capacidad_estudiantes'], 53)
    
    def test_promedio_calificaciones(self):
        data = {
            "calificaciones": [85, 92, 78, 96, 88]
        }
        response = self.client.post('/api/cursos/promedio-calificaciones/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['promedio_curso'], 87.8)
        self.assertEqual(response.data['nivel_rendimiento'], 'Muy Bueno')
    
    def test_calcular_progreso_estudiante(self):
        data = {
            "lecciones_completadas": 8,
            "total_lecciones": 10
        }
        response = self.client.post('/api/cursos/calcular-progreso-estudiante/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['porcentaje_progreso'], 80.0)
        self.assertEqual(response.data['estado_progreso'], 'Casi Terminando')
    
    def test_contar_estudiantes_aprobados(self):
        data = {
            "calificaciones": [45, 78, 92, 55, 88, 67],
            "nota_minima": 60
        }
        response = self.client.post('/api/cursos/contar-estudiantes-aprobados/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['estudiantes_aprobados'], 4)
        self.assertEqual(response.data['estudiantes_reprobados'], 2)
    
    def test_calcular_duracion_curso(self):
        data = {
            "modulos": 4,
            "lecciones_por_modulo": 5,
            "minutos_por_leccion": 45
        }
        response = self.client.post('/api/cursos/calcular-duracion-curso/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_lecciones'], 20)
        self.assertEqual(response.data['duracion_minutos'], 900)
        self.assertEqual(response.data['duracion_horas'], 15.0)