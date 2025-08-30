#Ejercicios FOR
# Serie incrementa y luego decrementa
# Entrada: N (número entero mayor a 1)
# Salida: 1, 2, ... N, N-1, N-2 ... 1

N = int(input())
resultado = []

# Primera parte: incrementa de 1 hasta N
for i in range(1, N + 1):
    resultado.append(str(i))

# Segunda parte: decrementa de N-1 hasta 1
for i in range(N - 1, 0, -1):
    resultado.append(str(i))

# Imprimir todos los números separados por coma y espacio
print(", ".join(resultado))