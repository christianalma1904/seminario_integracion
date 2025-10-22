"""
Pide salario y clasifica el cargo
<1000 junior
1000-2000 semi-junior
>2000 senior
"""

salario = int(input("Ingrese su salario"))


if salario <1000:
    cargo = "junior"
elif salario >2000:
    cargo ="senior"
else:
    cargo = "semi-senior"
    
print(f"Este es su cargo {cargo}")