#Este es un ejercicio visto en la clase para probar las diferencias entre for y while

valor = 1
while valor <= 5:
    print("Vuelta ", valor)
    valor += 1
print("termino")

for valor in range(1, 6):
    print("Vuelta ", valor)
print("termino")
