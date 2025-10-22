"""
Vacaciones por antiguedad
Pide años de antiguedad y muestra dias de vacaciones segun
<1=0
<3=3
<5=10
>=5=15

"""


antiguedad = int(input("Ingrese sus años de antiguedad: "))

if antiguedad < 1:
    vacaciones = 0
elif antiguedad < 3:
    vacaciones = 3
elif antiguedad < 5:
    vacaciones = 10
else:
    vacaciones = 15
    
print(f"Estos son sus dias de vacaciones {vacaciones}") 