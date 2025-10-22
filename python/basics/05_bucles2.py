"""
Pide el numero de empleados y el sueldo de cada uno
suma y muestra el total
"""

numeroe = int(input("Ingrese el numero de empleados"))

saldo = 0

for i in range(numeroe):
    sueldo = int(input("Ingrese el sueldo"))
    saldo += sueldo

print (saldo)