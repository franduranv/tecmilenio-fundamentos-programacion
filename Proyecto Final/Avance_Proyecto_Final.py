#Control de Contratos y Pagos - Edificio con 16 departamentos
#Avance de Proyecto Final - Fundamentos de Programación
#Alumno: Francisco José Durán Vargas
#Matricula: AL07193847
#Fecha de entrega: Lunes 1 de Septiembre del 2025 a las 23:59
#Programa: Ing. en Desarrollo de Software
#Materia: Fundamentos de Programación
#Docente: Jesús Carlos Morón García

"""
Control de Contratos y Pagos (Edificio con 16 departamentos)
-----------------------------------------------------------
Uso:
  1) Ejecuta el programa.
  2) Ingresa año y mes actuales (1..12).
  3) Ingresa cuántos contratos capturarás hoy.
  4) Por inquilino: nombre, depto, tipo (3/4), mes/año de contrato,
     renta histórica si aplica, meses y/o monto pagado en el año.
  5) Revisa el resumen por inquilino y el total del edificio.

Supuestos:
  - Corte mensual al día 1 (meses transcurridos = mes actual).
  - Tarifas estándar vigentes 2024–2025: 3 recámaras $7,500; 4 recámaras $8,500.
  - Si uno entre “meses pagados” o “monto pagado” es 0, se infiere con el otro.
"""


# ===============================================
# CLASES PRINCIPALES
# ===============================================

class BaseContract:
    """Clase base para todos los contratos"""
    def __init__(self, tenant_name, unit_code, start_month, start_year, monthly_rent):
        self.tenant_name = tenant_name
        self.unit_code = unit_code
        self.start_month = start_month
        self.start_year = start_year
        self.monthly_rent = monthly_rent
    
    def expected_due(self, month_current):
        """Calcula cuánto debería haber pagado hasta el mes actual"""
        return month_current * self.monthly_rent
    
    def infer_months_or_amount(self, months_paid, amount_paid):
        """Si uno de los valores es 0, lo calcula basado en el otro"""
        if months_paid == 0 and self.monthly_rent > 0:
            months_paid = amount_paid / self.monthly_rent
        elif amount_paid == 0:
            amount_paid = months_paid * self.monthly_rent
        return months_paid, amount_paid
    
    def balance(self, month_current, amount_paid):
        """Calcula si debe dinero o tiene saldo a favor"""
        expected = self.expected_due(month_current)
        difference = amount_paid - expected
        
        if difference < 0:
            debt = -difference
            favor = 0
        else:
            debt = 0
            favor = difference
        
        return expected, debt, favor


class StandardContract(BaseContract):
    """Contrato vigente 2024-2025 con tarifas estándar"""
    def __init__(self, tenant_name, unit_code, start_month, start_year, bedrooms):
        # Establecer renta según número de recámaras
        if bedrooms == 3:
            monthly_rent = 7500
        else:  # 4 recámaras
            monthly_rent = 8500
        
        super().__init__(tenant_name, unit_code, start_month, start_year, monthly_rent)
        self.bedrooms = bedrooms


class HistoricContract(BaseContract):
    """Contrato histórico con renta personalizada"""
    def __init__(self, tenant_name, unit_code, start_month, start_year, monthly_rent):
        super().__init__(tenant_name, unit_code, start_month, start_year, monthly_rent)


class BuildingManager:
    """Administra los contratos del edificio"""
    def __init__(self, current_year, current_month):
        self.current_year = current_year
        self.current_month = current_month
        self.total_building = 0
    
    def register_contracts(self, num_contracts):
        """Registra N contratos y calcula totales"""
        for i in range(1, num_contracts + 1):
            print(f"\n---------------------------------------------")
            print(f"Registro #{i}")
            
            # Datos básicos del inquilino
            name = input("Nombre del inquilino: ")
            unit = input("Clave del departamento (ej. D101, D202): ")
            
            # Validar tipo de departamento
            while True:
                bedrooms = int(input("Tipo de departamento (3 = tres recámaras, 4 = cuatro recámaras): "))
                if bedrooms in [3, 4]:
                    break
                print("Solo se permite 3 o 4 recámaras.")
            
            # Validar mes del contrato
            while True:
                contract_month = int(input("Mes del último contrato (1..12): "))
                if 1 <= contract_month <= 12:
                    break
                print("El mes debe estar entre 1 y 12.")
            
            contract_year = int(input("Año del último contrato (AAAA): "))
            
            # Crear contrato según vigencia
            if 2024 <= contract_year <= 2025:
                contract = StandardContract(name, unit, contract_month, contract_year, bedrooms)
            else:
                print("Contrato no actual (<> 2024-2025).")
                historic_rent = float(input("Ingresa la renta mensual estipulada en su contrato: "))
                contract = HistoricContract(name, unit, contract_month, contract_year, historic_rent)
            
            # Capturar pagos
            months_paid = float(input(f"Meses pagados en {self.current_year} (puede ser decimal, ej. 1.5). Si no lo sabes, ingresa 0: "))
            amount_paid = float(input(f"Monto pagado en {self.current_year} (si ya indicaste meses, ingresa 0): "))
            
            # Inferir dato faltante
            months_paid, amount_paid = contract.infer_months_or_amount(months_paid, amount_paid)
            
            # Calcular situación actual
            expected, debt, favor = contract.balance(self.current_month, amount_paid)
            self.total_building += amount_paid
            
            # Mostrar resumen
            print(f"\nResumen de {name} (Depto: {unit})")
            print(f"  Renta mensual: ${contract.monthly_rent}")
            print(f"  Meses transcurridos en {self.current_year}: {self.current_month}")
            print(f"  Meses pagados en {self.current_year}: {months_paid}")
            print(f"  Monto pagado en {self.current_year}: ${amount_paid}")
            print(f"  Debió pagar a la fecha: ${expected}")
            
            if debt > 0:
                print(f"  * Adeudo actual: ${debt}")
            if favor > 0:
                print(f"  * Saldo a favor: ${favor}")
    
    def show_total(self):
        """Muestra el total cobrado del edificio"""
        print(f"\n=============================================")
        print(f"TOTAL COBRADO EN {self.current_year}: ${self.total_building}")
        print(f"=============================================")


# ===============================================
# PROGRAMA PRINCIPAL
# ===============================================

def main():
    print("=== Control de Contratos y Pagos 2025 ===")
    
    # Contexto temporal
    current_year = int(input("Año actual (AAAA): "))
    
    while True:
        current_month = int(input("Mes actual (1..12): "))
        if 1 <= current_month <= 12:
            break
        print("El mes debe estar entre 1 y 12.")
    
    # Número de contratos
    num_contracts = int(input("¿Cuántos contratos registrarás hoy? "))
    
    # Procesar contratos
    manager = BuildingManager(current_year, current_month)
    manager.register_contracts(num_contracts)
    manager.show_total()


if __name__ == "__main__":
    main()