Algoritmo ControlContratos2025
	// Programa para controlar pagos de renta (edificio con 16 deptos)
	// ==============================================================
	// Declaración de variables
	Definir numContratos, i Como Entero
	Definir anioHoy, mesHoy Como Entero
	Definir tipoDep, contratoAnio, contratoMes Como Entero
	Definir mesesTranscurridos Como Entero
	Definir rentaMensual, montoPagado, mesesPagados Como Real
	Definir adeudoEsperado, diferencia, debe, saldoFavor, totalEdificio Como Real
	Definir nombre, depto Como Cadena
	
	// ==============================================================
	// Contexto temporal (año y mes actuales)
	Escribir "Año actual (AAAA):"
	Leer anioHoy
	
	Repetir
		Escribir "Mes actual (1..12):"
		Leer mesHoy
	Hasta Que mesHoy >= 1 Y mesHoy <= 12
	
	// ==============================================================
	// Cantidad de contratos a registrar
	Escribir "¿Cuántos contratos registrarás hoy?"
	Leer numContratos
	
	totalEdificio <- 0
	
	// ==============================================================
	// Bucle principal por contrato/inquilino
	Para i <- 1 Hasta numContratos Hacer
		
		Escribir ""
		Escribir "---------------------------------------------"
		Escribir "Registro #", i
		
		Escribir "Nombre del inquilino:"
		Leer nombre
		
		Escribir "Clave del departamento (ej. D101, D202):"
		Leer depto
		
		// Validación tipo de depto 3/4 recámaras
		Repetir
			Escribir "Tipo de departamento (3 = tres recámaras, 4 = cuatro recámaras):"
			Leer tipoDep
		Hasta Que tipoDep = 3 O tipoDep = 4
		
		// Validación simple de mes de contrato
		Repetir
			Escribir "Mes del último contrato (1..12):"
			Leer contratoMes
		Hasta Que contratoMes >= 1 Y contratoMes <= 12
		
		Escribir "Año del último contrato (AAAA):"
		Leer contratoAnio
		
		// ==============================================================
		// DECISIÓN 1: ¿El contrato es vigente 2024-2025?
		Si (contratoAnio >= 2024 Y contratoAnio <= 2025) Entonces
			Si tipoDep = 3 Entonces
				rentaMensual <- 7500
			Sino
				rentaMensual <- 8500
			FinSi
		Sino
			Escribir "Contrato no actual (<> 2024-2025)."
			Escribir "Ingresa la renta mensual estipulada en su contrato:"
			Leer rentaMensual
		FinSi
		
		// ==============================================================
		// Captura pagos del año en curso (enero..mesHoy)
		Escribir "Meses pagados en ", anioHoy, " (puede ser decimal, ej. 1.5). Si no lo sabes, ingresa 0:"
		Leer mesesPagados
		
		Escribir "Monto pagado en ", anioHoy, " (si ya indicaste meses, ingresa 0):"
		Leer montoPagado
		
		// ==============================================================
		// DECISIÓN 2 (tabla de verdad simple): calcular el faltante si uno es 0
		Si mesesPagados = 0 Entonces
			Si rentaMensual > 0 Entonces
				mesesPagados <- montoPagado / rentaMensual
			Sino
				mesesPagados <- 0
			FinSi
		FinSi
		
		Si montoPagado = 0 Entonces
			montoPagado <- mesesPagados * rentaMensual
		FinSi
		
		// ==============================================================
		// Cálculo de situación a la fecha
		mesesTranscurridos <- mesHoy
		adeudoEsperado <- mesesTranscurridos * rentaMensual
		diferencia <- montoPagado - adeudoEsperado
		
		Si diferencia < 0 Entonces
			debe <- -diferencia
			saldoFavor <- 0
		Sino
			debe <- 0
			saldoFavor <- diferencia
		FinSi
		
		totalEdificio <- totalEdificio + montoPagado
		
		// ==============================================================
		// Salida/resumen por inquilino
		Escribir ""
		Escribir "Resumen de ", nombre, " (Depto: ", depto, ")"
		Escribir "  Renta mensual: $", rentaMensual
		Escribir "  Meses transcurridos en ", anioHoy, ": ", mesesTranscurridos
		Escribir "  Meses pagados en ", anioHoy, ": ", mesesPagados
		Escribir "  Monto pagado en ", anioHoy, ": $", montoPagado
		Escribir "  Debió pagar a la fecha: $", adeudoEsperado
		
		Si debe > 0 Entonces
			Escribir "  * Adeudo actual: $", debe
		FinSi
		Si saldoFavor > 0 Entonces
			Escribir "  * Saldo a favor: $", saldoFavor
		FinSi
		
	FinPara
	
	// ==============================================================
	// Totales del edificio en el año actual
	Escribir ""
	Escribir "============================================="
	Escribir "TOTAL COBRADO EN ", anioHoy, ": $", totalEdificio
	Escribir "============================================="
FinAlgoritmo
