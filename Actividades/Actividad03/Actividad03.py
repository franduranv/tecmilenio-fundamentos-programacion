# Actividad 03 - Tabla de Pitágoras
# Alumno: Francisco José Durán Vargas
# Matrícula: AL07193847
# Materia: Fundamentos de Programación
# Docente: Jesús Carlos Morón García
# Fecha de entrega: Septiembre 2025

# =====================================
# Función para generar la tabla (matriz)
# =====================================

def generar_tabla(n=10):
    tabla = []
    for i in range(1, n+1):
        fila = []
        for j in range(1, n+1):
            fila.append(i * j)  # construcción de la tabla
        tabla.append(fila)
    return tabla

# =====================================
# Función que NO regresa valor (imprime tabla)
# =====================================
def mostrar_tabla(tabla):
    print("\nTABLA DE PITÁGORAS\n")
    for fila in tabla:
        for valor in fila:
            print(f"{valor:4}", end="")  # alineado en columnas
        print()  # salto de línea por fila

# =====================================
# Función que regresa valor (multiplicación)
# =====================================
def multiplicar(tabla, a, b):
    # Como las listas empiezan en 0, restamos 1 a cada índice
    return tabla[a-1][b-1]

# =====================================
# Programa principal
# =====================================
def main():
    tabla = generar_tabla(10)
    mostrar_tabla(tabla)

    print("\n=== Multiplicación con tabla de Pitágoras ===")
    a = int(input("Ingresa el primer factor (1-10): "))
    b = int(input("Ingresa el segundo factor (1-10): "))

    resultado = multiplicar(tabla, a, b)
    print(f"\nEl resultado de {a} x {b} es: {resultado}")

# =====================================
# Punto de entrada
# =====================================
if __name__ == "__main__":
    main()