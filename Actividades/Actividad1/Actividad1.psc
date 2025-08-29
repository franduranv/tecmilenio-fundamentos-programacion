Algoritmo Actvidad1
	// Solicita al nombre de usuario su nombre
	Escribir 'Ingresa su nombre: '
	Leer userName
	// Captura el numero de horas por categoria
	Escribir 'Ingrese numero de horas en Redes Sociales: '
	Leer redesSociales
	Escribir 'Ingrese numero de horas en Mensajes: '
	Leer mensajes
	Escribir 'Ingrese numero de horas en Series de Television: '
	Leer series
	Escribir 'Ingrese numero de horas en Series de Video: '
	Leer videos
	Escribir 'Ingrese numero de horas en Series de Videojuegos: '
	Leer juegos
	// Suma el total de horas
	total <- redesSociales+mensajes+series+videos+juegos
	// lo convierte a porcentaje de un dia
	porcentaje <- (total/24)*100
	// Muestra al usuario el total de horas y %
	Escribir 'Hola ', userName, ', has usado ', total, ' horas en plataformas digitales.'
	Escribir 'Esto representa un ', porcentaje, '% del día.'
FinAlgoritmo
