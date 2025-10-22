"""
Escribe un pograma que pida edad, años de experiencia y si tiene titulo universitario
un candidato es elegible, si tiene >=21 años y experencia >= 2 años o titulo
Muestra elegible o no elegible
"""

edad = int(input("Edad del candidato"))
exp = int(input("Años de experiencia"))
tiene_titulo = input("tiene titulo universitario? s/n").lower()=="s"

if (edad >= 21 and (exp >= 2 or tiene_titulo == "s")):
    print ("elegible")
else:
    print ("no elegible")
    