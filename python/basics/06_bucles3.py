"""
Pide numero de empleados
cada empleado solicita nombre y salario
determina quien tiene el mayor salario y muestralo
"""
numeroe = int(input("Escriba el numero de empleados "))
salario2 = 0
for i in range(numeroe):
    nombre = input("Ingrese el nombre ")
    salario = int(input("Ingrese el salario "))
    if salario >= salario2:
        salario2 = salario
    else:
        salario2 = salario2
        
print(f"Este es el mayor salario {salario2}")