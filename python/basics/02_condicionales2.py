"""
Sistema que pida el pago por hora y horas trabajadas
las primeras 40 h son normales, las extras se las paga al 150%
Calcula y muestra el total semanal
"""

horast = int(input("Escribe el total de horas en la semana "))
pagoh = int(input("Ingresa el pago por hora "))

if horast > 40:
    extras = pagoh * 1.5
else:
    extras = pagoh
    
totals = horast * extras

print(f"Este es tu pago semanal {totals} por tus horas trabajadas")
