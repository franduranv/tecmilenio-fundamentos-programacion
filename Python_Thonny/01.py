# Solicitar un numero al usuario
numero = int(input("Ingrese un número entero: "))

# Determinar si es par o impar
if numero % 2 == 0:
    if numero >= 0:
        print("Par positivo")
    else:
        print("Par negativo")
else:
    if numero > 0:
        print("Impar positivo")
    else:
        print("Impar negativo")