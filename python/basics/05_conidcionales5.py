"""
Pide salario y desempeño (1-5)
si el desempeño es:

>4 = 15%
>3 = 10%
>2 = 5%
>1 = 2%
"""


desempeño = int(input("Ingrese su desemepeño entre 1-5"))
salario = int(input("Ingrese el salario "))

if desempeño == 1:
    bonus = salario * 0.02
elif desempeño == 2:
    bonus = salario * 0.05
elif desempeño  == 3:
    bonus = salario * 0.10
elif desempeño == 4:
    bonus = salario * 0.15
else:
    bonus = 0
    
total = salario + bonus

print(total)