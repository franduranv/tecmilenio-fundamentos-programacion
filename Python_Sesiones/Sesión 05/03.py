
# Aplicaciones: Calcular promedios, totales de ventas, puntuaciones acumuladas,
# estadísticas deportivas, análisis financiero, contadores de progreso,
# sistemas de calificación, cálculos matemáticos básicos y series aritméticas

numero = int(input("Ingresa un número: "))
suma = 0
for i in range(1, numero + 1):
    suma += i
print("La suma de los números desde 1 hasta", numero, "es:", suma)
