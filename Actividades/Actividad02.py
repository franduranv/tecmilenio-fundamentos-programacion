# Actividad 02 - Cobro de entradas al Museo
# Alumno: Francisco José Durán Vargas
# Matricula: AL07193847
# Fecha de entrega: Lunes 25 de Agosto

print("Bienvenido al sistema de entradas del Museo de Arte e Historia de Guanajuato\n")

total_pagar = 0
contador_visitantes = 0

while True:
    try:
        edad = int(input("Ingrese la edad del visitante: "))
    except ValueError:
        print("Por favor, ingrese un número válido para la edad.\n")
        continue

    if edad < 3:
        print("El visitante entra gratis por ser menor de 3 años.\n")
        continue  # No se contabiliza ni se cobra

    # Precio base por edad
    precio = 30 if edad < 18 else 45

    # Descuento
    if edad >= 60:
        descuento = 0.12
        print("Descuento aplicado: Adulto mayor (12%)")
    else:
        respuesta = input("¿Es estudiante o profesor? (s/n): ").lower()
        descuento = 0.10 if respuesta == 's' else 0.0
        if descuento > 0:
            print("Descuento aplicado: Estudiante o Profesor (10%)")

    pago = precio * (1 - descuento)
    total_pagar += pago
    contador_visitantes += 1

    print(f"Pago por este visitante: ${pago:,.2f}\n")

    continuar = input("¿Desea registrar a otro visitante? (s/n): ").lower()
    if continuar != 's':
        break

# Mostrar resumen final
print(f"\nSe registraron {contador_visitantes} visitantes.")
print(f"Total a pagar: ${total_pagar:,.2f}")