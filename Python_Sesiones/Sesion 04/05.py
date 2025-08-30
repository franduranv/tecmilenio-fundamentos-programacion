suma = 0
numero = 1

while numero != 0:
    numero = int(input("Ingresa un número (0 para terminar): "))
    if numero != 0:
        suma += numero
    print("La suma total es:", suma)