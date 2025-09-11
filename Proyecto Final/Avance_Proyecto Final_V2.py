"""
Sistema de Control de Contratos de Renta - Edificio Residencial
=============================================================
Autor: [Tu Nombre]
Materia: Fundamentos de Programación
Universidad: TecMilenio

Este programa implementa un sistema orientado a objetos para el control
de pagos de renta de un edificio con 16 departamentos.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple


class BaseContract(ABC):
    """
    Clase base abstracta que define los atributos y métodos comunes
    para todos los tipos de contratos de renta.
    """
    
    def __init__(self, tenant_name: str, unit_code: str, start_month: int, 
                 start_year: int, monthly_rent: float):
        """
        Inicializa un contrato base.
        
        Args:
            tenant_name (str): Nombre del inquilino
            unit_code (str): Código del departamento (ej. D101, D202)
            start_month (int): Mes de inicio del contrato (1-12)
            start_year (int): Año de inicio del contrato
            monthly_rent (float): Renta mensual
        """
        self.tenant_name = tenant_name
        self.unit_code = unit_code
        self.start_month = start_month
        self.start_year = start_year
        self.monthly_rent = monthly_rent
        self._paid_months = 0.0
        self._paid_amount = 0.0
    
    def set_payments(self, paid_months: float = 0.0, paid_amount: float = 0.0):
        """
        Establece los pagos realizados en el año actual.
        
        Args:
            paid_months (float): Meses pagados
            paid_amount (float): Monto pagado
        """
        self._paid_months = paid_months
        self._paid_amount = paid_amount
    
    def infer_months_or_amount(self) -> Tuple[float, float]:
        """
        Infiere los meses pagados o el monto pagado basándose en el otro valor.
        Si meses_pagados = 0, infiere por monto.
        Si monto = 0, infiere por meses.
        
        Returns:
            Tuple[float, float]: (meses_pagados, monto_pagado)
        """
        if self._paid_months == 0 and self.monthly_rent > 0:
            self._paid_months = self._paid_amount / self.monthly_rent
        
        if self._paid_amount == 0:
            self._paid_amount = self._paid_months * self.monthly_rent
            
        return self._paid_months, self._paid_amount
    
    def expected_due(self, current_month: int) -> float:
        """
        Calcula el adeudo esperado hasta el mes actual.
        
        Args:
            current_month (int): Mes actual (1-12)
            
        Returns:
            float: Monto que debería haber pagado hasta la fecha
        """
        return current_month * self.monthly_rent
    
    def balance(self, current_month: int) -> Tuple[float, float]:
        """
        Calcula el balance del contrato (adeudo o saldo a favor).
        
        Args:
            current_month (int): Mes actual
            
        Returns:
            Tuple[float, float]: (adeudo, saldo_a_favor)
        """
        # Asegurar que los valores están actualizados
        self.infer_months_or_amount()
        
        expected_amount = self.expected_due(current_month)
        difference = self._paid_amount - expected_amount
        
        if difference < 0:
            return -difference, 0.0  # Tiene adeudo
        else:
            return 0.0, difference   # Tiene saldo a favor
    
    def get_payment_info(self) -> Tuple[float, float]:
        """
        Obtiene la información de pagos actuales.
        
        Returns:
            Tuple[float, float]: (meses_pagados, monto_pagado)
        """
        return self._paid_months, self._paid_amount
    
    @abstractmethod
    def get_contract_type(self) -> str:
        """
        Método abstracto que debe ser implementado por las clases hijas
        para identificar el tipo de contrato.
        """
        pass


class StandardContract(BaseContract):
    """
    Contrato estándar para periodos 2024-2025.
    La renta mensual se fija automáticamente según el número de recámaras.
    """
    
    def __init__(self, tenant_name: str, unit_code: str, start_month: int, 
                 start_year: int, bedrooms: int):
        """
        Inicializa un contrato estándar.
        
        Args:
            tenant_name (str): Nombre del inquilino
            unit_code (str): Código del departamento
            start_month (int): Mes de inicio del contrato
            start_year (int): Año de inicio del contrato
            bedrooms (int): Número de recámaras (3 o 4)
        """
        # Establecer renta según número de recámaras
        if bedrooms == 3:
            monthly_rent = 7500.0
        elif bedrooms == 4:
            monthly_rent = 8500.0
        else:
            raise ValueError("Los departamentos solo pueden ser de 3 o 4 recámaras")
        
        super().__init__(tenant_name, unit_code, start_month, start_year, monthly_rent)
        self.bedrooms = bedrooms
    
    def get_contract_type(self) -> str:
        """
        Retorna el tipo de contrato.
        
        Returns:
            str: Tipo de contrato
        """
        return f"Estándar 2024-2025 ({self.bedrooms} recámaras)"


class HistoricContract(BaseContract):
    """
    Contrato histórico (anterior a 2024 o posterior a 2025).
    La renta mensual es ingresada manualmente por el usuario.
    """
    
    def __init__(self, tenant_name: str, unit_code: str, start_month: int, 
                 start_year: int, monthly_rent: float):
        """
        Inicializa un contrato histórico.
        
        Args:
            tenant_name (str): Nombre del inquilino
            unit_code (str): Código del departamento
            start_month (int): Mes de inicio del contrato
            start_year (int): Año de inicio del contrato
            monthly_rent (float): Renta mensual del contrato original
        """
        super().__init__(tenant_name, unit_code, start_month, start_year, monthly_rent)
    
    def get_contract_type(self) -> str:
        """
        Retorna el tipo de contrato.
        
        Returns:
            str: Tipo de contrato
        """
        return f"Histórico ({self.start_year})"


class BuildingManager:
    """
    Clase que orquesta la captura de N contratos, calcula adeudos/saldos
    y el total anual del edificio.
    """
    
    def __init__(self, current_year: int, current_month: int):
        """
        Inicializa el administrador del edificio.
        
        Args:
            current_year (int): Año actual
            current_month (int): Mes actual (1-12)
        """
        self.current_year = current_year
        self.current_month = current_month
        self.contracts: List[BaseContract] = []
    
    def add_contract(self, contract: BaseContract):
        """
        Agrega un contrato a la lista de contratos administrados.
        
        Args:
            contract (BaseContract): Contrato a agregar
        """
        self.contracts.append(contract)
    
    def create_contract_interactive(self) -> BaseContract:
        """
        Crea un contrato de forma interactiva solicitando datos al usuario.
        
        Returns:
            BaseContract: Contrato creado
        """
        print(f"\n{'-'*45}")
        print(f"Registro #{len(self.contracts) + 1}")
        
        # Datos básicos del inquilino
        tenant_name = input("Nombre del inquilino: ").strip()
        unit_code = input("Clave del departamento (ej. D101, D202): ").strip()
        
        # Validación tipo de departamento
        while True:
            try:
                bedrooms = int(input("Tipo de departamento (3 = tres recámaras, 4 = cuatro recámaras): "))
                if bedrooms in [3, 4]:
                    break
                else:
                    print("Error: Solo se permiten departamentos de 3 o 4 recámaras.")
            except ValueError:
                print("Error: Ingrese un número válido (3 o 4).")
        
        # Validación mes del contrato
        while True:
            try:
                contract_month = int(input("Mes del último contrato (1..12): "))
                if 1 <= contract_month <= 12:
                    break
                else:
                    print("Error: El mes debe estar entre 1 y 12.")
            except ValueError:
                print("Error: Ingrese un número válido.")
        
        # Año del contrato
        while True:
            try:
                contract_year = int(input("Año del último contrato (AAAA): "))
                break
            except ValueError:
                print("Error: Ingrese un año válido.")
        
        # Decidir tipo de contrato según el año
        if 2024 <= contract_year <= 2025:
            contract = StandardContract(tenant_name, unit_code, contract_month, 
                                      contract_year, bedrooms)
            print(f"Contrato estándar 2024-2025. Renta mensual: ${contract.monthly_rent:,.2f}")
        else:
            print("Contrato no actual (<> 2024-2025).")
            while True:
                try:
                    monthly_rent = float(input("Ingresa la renta mensual estipulada en su contrato: $"))
                    if monthly_rent > 0:
                        break
                    else:
                        print("Error: La renta debe ser mayor a 0.")
                except ValueError:
                    print("Error: Ingrese un monto válido.")
            
            contract = HistoricContract(tenant_name, unit_code, contract_month, 
                                      contract_year, monthly_rent)
        
        # Captura de pagos
        print(f"\nCaptura de pagos en {self.current_year}:")
        
        while True:
            try:
                paid_months = float(input(f"Meses pagados en {self.current_year} (puede ser decimal, ej. 1.5). Si no lo sabes, ingresa 0: "))
                if paid_months >= 0:
                    break
                else:
                    print("Error: Los meses pagados no pueden ser negativos.")
            except ValueError:
                print("Error: Ingrese un número válido.")
        
        while True:
            try:
                paid_amount = float(input(f"Monto pagado en {self.current_year} (si ya indicaste meses, ingresa 0): $"))
                if paid_amount >= 0:
                    break
                else:
                    print("Error: El monto pagado no puede ser negativo.")
            except ValueError:
                print("Error: Ingrese un monto válido.")
        
        # Establecer pagos y calcular valores faltantes
        contract.set_payments(paid_months, paid_amount)
        
        return contract
    
    def display_contract_summary(self, contract: BaseContract):
        """
        Muestra el resumen de un contrato específico.
        
        Args:
            contract (BaseContract): Contrato a mostrar
        """
        paid_months, paid_amount = contract.get_payment_info()
        adeudo, saldo_favor = contract.balance(self.current_month)
        expected_amount = contract.expected_due(self.current_month)
        
        print(f"\nResumen de {contract.tenant_name} (Depto: {contract.unit_code})")
        print(f"  Tipo de contrato: {contract.get_contract_type()}")
        print(f"  Renta mensual: ${contract.monthly_rent:,.2f}")
        print(f"  Meses transcurridos en {self.current_year}: {self.current_month}")
        print(f"  Meses pagados en {self.current_year}: {paid_months:.2f}")
        print(f"  Monto pagado en {self.current_year}: ${paid_amount:,.2f}")
        print(f"  Debió pagar a la fecha: ${expected_amount:,.2f}")
        
        if adeudo > 0:
            print(f"  * Adeudo actual: ${adeudo:,.2f}")
        if saldo_favor > 0:
            print(f"  * Saldo a favor: ${saldo_favor:,.2f}")
    
    def calculate_building_total(self) -> float:
        """
        Calcula el total cobrado en el edificio durante el año actual.
        
        Returns:
            float: Total cobrado en el año
        """
        total = 0.0
        for contract in self.contracts:
            _, paid_amount = contract.get_payment_info()
            total += paid_amount
        return total
    
    def run_building_management(self):
        """
        Ejecuta el flujo principal de administración del edificio.
        """
        print("Sistema de Control de Contratos de Renta")
        print("======================================")
        print(f"Año actual: {self.current_year}")
        print(f"Mes actual: {self.current_month}")
        
        # Solicitar número de contratos
        while True:
            try:
                num_contracts = int(input("\n¿Cuántos contratos registrarás hoy? "))
                if num_contracts > 0:
                    break
                else:
                    print("Error: Debe registrar al menos un contrato.")
            except ValueError:
                print("Error: Ingrese un número válido.")
        
        # Registrar contratos
        for i in range(num_contracts):
            contract = self.create_contract_interactive()
            self.add_contract(contract)
            self.display_contract_summary(contract)
        
        # Mostrar totales del edificio
        total_collected = self.calculate_building_total()
        print(f"\n{'='*45}")
        print(f"TOTAL COBRADO EN {self.current_year}: ${total_collected:,.2f}")
        print(f"{'='*45}")
        
        # Estadísticas adicionales
        print(f"\nEstadísticas del edificio:")
        print(f"  Contratos registrados: {len(self.contracts)}")
        
        contracts_with_debt = sum(1 for contract in self.contracts 
                                if contract.balance(self.current_month)[0] > 0)
        contracts_with_credit = sum(1 for contract in self.contracts 
                                  if contract.balance(self.current_month)[1] > 0)
        
        print(f"  Contratos con adeudo: {contracts_with_debt}")
        print(f"  Contratos con saldo a favor: {contracts_with_credit}")
        print(f"  Contratos al corriente: {len(self.contracts) - contracts_with_debt - contracts_with_credit}")


def validate_month(month: int) -> bool:
    """
    Valida que el mes esté en el rango correcto.
    
    Args:
        month (int): Mes a validar
        
    Returns:
        bool: True si el mes es válido
    """
    return 1 <= month <= 12


def main():
    """
    Función principal del programa.
    """
    print("Programa para controlar pagos de renta (edificio con 16 deptos)")
    print("==============================================================")
    
    # Captura del contexto temporal
    while True:
        try:
            current_year = int(input("Año actual (AAAA): "))
            if current_year > 0:
                break
            else:
                print("Error: Ingrese un año válido.")
        except ValueError:
            print("Error: Ingrese un año válido.")
    
    while True:
        try:
            current_month = int(input("Mes actual (1..12): "))
            if validate_month(current_month):
                break
            else:
                print("Error: El mes debe estar entre 1 y 12.")
        except ValueError:
            print("Error: Ingrese un número válido.")
    
    # Crear y ejecutar el administrador del edificio
    building_manager = BuildingManager(current_year, current_month)
    building_manager.run_building_management()


if __name__ == "__main__":
    main()
