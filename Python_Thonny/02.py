# Solicitar los tres lados
x = int(input("Ingresa la longitud del lado X: "))
y = int(input("Ingresa la longitud del lado Y: "))
z = int(input("Ingresa la longitud del lado Z: "))

# Validar que los lados sean mayores que cero
if x > 0 and y > 0 and z > 0:
    # Verificar la desigualdad triangular
    if (x + y > z) and (x + z > y) and (y + z > x):
        # Determinar tipo de triángulo
        if x == y == z:
            print("Triángulo equilátero")
        elif x == y or x == z or y == z:
            print("Triángulo isósceles")
        else:
            print("Triángulo escaleno")
    else:
        print("No es un triángulo: no cumple con la desigualdad triangular.")
else:
    print("No es un triángulo: los lados deben ser mayores que cero.")