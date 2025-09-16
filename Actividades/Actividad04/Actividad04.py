# Actividad 04 – Tuplas, Diccionarios, Excepciones y Strings
# Alumno: Francisco José Durán Vargas
# Matrícula: AL07193847
# Materia: Fundamentos de Programación
# Docente: Jesús Carlos Morón García
# Fecha de entrega: Septiembre 2025
# =====================================

# -----------------------------
# Funciones auxiliares (genéricas)
# -----------------------------
def pausa():
    input("\nPresiona ENTER para continuar...")


# -----------------------------
# 1) TUPLAS
# -----------------------------
def suma_tupla(numeros: tuple) -> float:
    """Suma manual (sin usar sum()) de una tupla de números."""
    total = 0
    for n in numeros:
        try:
            total += n
        except TypeError:
            print(f"Advertencia: '{n}' no es un número, se omite.")
            continue
    return total


def demo_tuplas():
    print("\n=== DEMO: TUPLAS ===")
    print("📋 Definiendo tupla con 5 frutas...")
    
    # 1) DEFINICIÓN: Tupla con al menos 5 frutas (inmutable)
    frutas = ("manzana", "pera", "uva", "mango", "plátano")
    print(f"Tupla original: {frutas}")

    # 2) MANIPULACIÓN: Acceso por índice - Tercer elemento (índice 2)
    print(f"✅ Tercer elemento (índice 2): '{frutas[2]}'")

    # 3) CAPTURA: Dos frutas adicionales del usuario
    print("\n🔹 Agregando frutas nuevas...")
    f1 = input("Ingresa nueva fruta 1: ").strip()
    f2 = input("Ingresa nueva fruta 2: ").strip()
    
    # 4) MODIFICACIÓN: Tuplas son inmutables → concatenación para "modificar"
    frutas_expandida = frutas + (f1, f2)
    print(f"Tupla expandida: {frutas_expandida}")

    # 5) EXTRACCIÓN y MANIPULACIÓN: Convertir a lista, ordenar y mostrar
    lista_frutas = list(frutas_expandida)
    lista_frutas.sort()  # Ordenamiento alfabético
    print(f"✅ Frutas ordenadas: {', '.join(lista_frutas)}")

    # 6) FUNCIÓN PERSONALIZADA: Suma de longitudes usando función que recibe tupla
    longitudes = tuple(len(fruta) for fruta in lista_frutas)
    print(f"Tupla de longitudes: {longitudes}")
    total_letras = suma_tupla(longitudes)
    print(f"✅ Total de caracteres en nombres de frutas: {total_letras}")
    pausa()


# -----------------------------
# 2) DICCIONARIOS
# -----------------------------
def buscar_contacto(contactos: dict, nombre: str):
    """Retorna el teléfono del contacto (o None si no existe)."""
    return contactos.get(nombre)


def demo_diccionarios():
    print("\n=== DEMO: DICCIONARIOS ===")
    print("📋 Definiendo diccionario de contactos...")
    
    # 1) DEFINICIÓN: Diccionario base con 3 contactos
    contactos = {
        "Ana": "555-111-2222",
        "Luis": "555-333-4444",
        "Mara": "555-555-6666",
    }
    print(f"Diccionario inicial: {contactos}")

    # 2) CAPTURA y MANIPULACIÓN: Agregar nuevo contacto
    print("\n🔹 Agregando nuevo contacto...")
    nom = input("Nombre del nuevo contacto: ").strip()
    tel = input("Teléfono del nuevo contacto: ").strip()
    contactos[nom] = tel  # Modificación del diccionario
    print(f"✅ Contacto '{nom}' agregado exitosamente")

    # 3) EXTRACCIÓN: Iterar claves e imprimir nombres
    print("\n📇 Contactos registrados:")
    for nombre in contactos.keys():
        print(f"   • {nombre}")

    # 4) FUNCIÓN PERSONALIZADA y MANIPULACIÓN: Búsqueda de contacto
    print("\n🔍 Función de búsqueda:")
    buscado = input("¿A quién deseas buscar?: ").strip()
    tel_encontrado = buscar_contacto(contactos, buscado)
    
    if tel_encontrado is None:
        print(f"❌ No se encontró el contacto: {buscado}")
    else:
        print(f"✅ Teléfono de {buscado}: {tel_encontrado}")
    
    # MANIPULACIÓN adicional: Mostrar total de contactos
    print(f"\n📊 Total de contactos almacenados: {len(contactos)}")
    pausa()


# -----------------------------
# 3) EXCEPCIONES
# -----------------------------
class DivisionEntreCeroError(Exception):
    """Excepción personalizada para división entre cero."""
    pass


def demo_excepciones():
    print("\n=== DEMO: EXCEPCIONES ===")
    print("🛡️ Manejo robusto de excepciones...")
    
    # MANEJO DE EXCEPCIONES: Try-except para entrada no numérica
    try:
        print("\n📝 Ingresa dos números enteros:")
        a = int(input("Número entero A: ").strip())
        b = int(input("Número entero B: ").strip())
        print(f"✅ Números capturados correctamente: A={a}, B={b}")
        
    except ValueError as e:
        print(f"❌ Error de valor: {e}")
        print("⚠️  EXCEPCIÓN MANEJADA: Entrada no numérica detectada")
        print("💡 Debes ingresar valores ENTEROS válidos.")
        pausa()
        return
    except KeyboardInterrupt:
        print("\n⚠️  Operación cancelada por el usuario.")
        pausa()
        return

    # MANIPULACIÓN: Operación suma (siempre funciona)
    resultado_suma = a + b
    print(f"🔢 Suma A + B = {resultado_suma}")

    # EXCEPCIÓN PERSONALIZADA: División entre cero
    print("\n🔄 Probando división con excepción personalizada...")
    try:
        if b == 0:
            raise DivisionEntreCeroError("División entre cero detectada")
        
        division = a / b
        print(f"✅ División A / B = {division:.2f}")
        
    except DivisionEntreCeroError as e:
        print(f"❌ EXCEPCIÓN PERSONALIZADA CAPTURADA: {e}")
        print("⚠️  El manejo de excepciones funcionó correctamente")
    
    print("🛡️ Demostración de manejo robusto completada")
    pausa()


# -----------------------------
# 4) STRINGS
# -----------------------------
def contar_palabras(s: str) -> int:
    """
    Cuenta palabras separadas por espacios (ignora múltiples espacios).
    También maneja signos de puntuación básicos.
    """
    if not s.strip():  # Cadena vacía o solo espacios
        return 0
    # split() sin argumentos separa por cualquier cantidad de espacios
    palabras = [word.strip('.,!?;:') for word in s.split() if word.strip('.,!?;:')]
    return len(palabras)


def demo_strings():
    print("\n=== DEMO: STRINGS ===")
    print("📝 Manipulación completa de cadenas de texto...")
    
    # CAPTURA: Obtener mensaje del usuario
    mensaje = input("Escribe un mensaje: ").strip()
    if not mensaje:
        mensaje = "Este es un mensaje de ejemplo para demostrar strings."
        print(f"💡 Usando mensaje por defecto: '{mensaje}'")

    # MANIPULACIÓN 1: Calcular longitud
    longitud = len(mensaje)
    print(f"📏 Longitud del mensaje: {longitud} caracteres")

    # MANIPULACIÓN 2: Conversión a mayúsculas
    mensaje_mayus = mensaje.upper()
    print(f"🔠 MAYÚSCULAS: {mensaje_mayus}")

    # MANIPULACIÓN 3: Reemplazo de palabras
    print("\n🔄 Función de reemplazo:")
    vieja = input("Palabra a reemplazar (tal como aparece): ").strip()
    nueva = input("Nueva palabra: ").strip()
    
    if vieja in mensaje:
        mensaje_reemplazado = mensaje.replace(vieja, nueva)
        print(f"✅ Reemplazado: '{mensaje_reemplazado}'")
    else:
        print(f"⚠️  La palabra '{vieja}' no se encontró en el mensaje")
        mensaje_reemplazado = mensaje

    # FUNCIÓN PERSONALIZADA: Contar palabras
    print("\n🔢 Función personalizada de conteo:")
    total_palabras = contar_palabras(mensaje)
    print(f"✅ Cantidad de palabras en el mensaje original: {total_palabras}")
    
    # MANIPULACIÓN adicional: Otras operaciones con strings
    print(f"📊 Análisis adicional del mensaje:")
    print(f"   • Minúsculas: '{mensaje.lower()}'")
    print(f"   • Primera letra mayúscula: '{mensaje.capitalize()}'")
    print(f"   • ¿Contiene números?: {'Sí' if any(c.isdigit() for c in mensaje) else 'No'}")
    pausa()


# -----------------------------
# MENÚ PRINCIPAL
# -----------------------------
def main():
    print("🔹" * 50)
    print("   ACTIVIDAD 04: TUPLAS, DICCIONARIOS, EXCEPCIONES Y STRINGS")
    print("   Alumno: Francisco José Durán Vargas")
    print("🔹" * 50)
    
    while True:
        print("\n" + "=" * 30 + " MENÚ PRINCIPAL " + "=" * 30)
        print("│  1️⃣  Tuplas")
        print("│  2️⃣  Diccionarios")
        print("│  3️⃣  Excepciones")
        print("│  4️⃣  Strings")
        print("│  5️⃣  Salir")
        print("═" * 76)

        try:
            opcion = input("🎯 Elige una opción (1-5): ").strip()
            
            if opcion == "1":
                demo_tuplas()
            elif opcion == "2":
                demo_diccionarios()
            elif opcion == "3":
                demo_excepciones()
            elif opcion == "4":
                demo_strings()
            elif opcion == "5":
                print("\n✅ ¡Programa finalizado correctamente!")
                print("📚 Gracias por usar esta aplicación educativa.")
                break
            else:
                print("❌ Opción inválida. Por favor, elige un número del 1 al 5.")
                
        except KeyboardInterrupt:
            print("\n\n⚠️  Programa interrumpido por el usuario.")
            print("✅ ¡Hasta la vista!")
            break
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            print("🔄 Intentando continuar...")


if __name__ == "__main__":
    main()