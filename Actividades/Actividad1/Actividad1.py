# Solicita al usuario su nombre
userName = input("Ingresa su nombre: ")

# Captura el número de horas por categoría
redesSociales = float(input("Ingrese número de horas en Redes Sociales: "))
mensajes = float(input("Ingrese número de horas en Mensajes: "))
series = float(input("Ingrese número de horas en Series de Televisión: "))
videos = float(input("Ingrese número de horas en Videos: "))
juegos = float(input("Ingrese número de horas en Videojuegos: "))

# Suma el total de horas
total = redesSociales + mensajes + series + videos + juegos

# Lo convierte a porcentaje de un día
porcentaje = (total / 24) * 100

# Muestra al usuario el total de horas y el porcentaje
print(f"Hola {userName}, has usado {total:.2f} horas en plataformas digitales.")
print(f"Esto representa un {porcentaje:.2f}% del día.")