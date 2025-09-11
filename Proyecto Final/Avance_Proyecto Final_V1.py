"""
Control de Contratos y Pagos (Edificio con 16 departamentos)
============================================================

Objetivo
--------
Registrar N inquilinos/contratos, aplicar política de renta vigente
(2024–2025: 3 recámaras=$7,500; 4 recámaras=$8,500) o renta histórica
(en prórroga), capturar pagos del año actual (en meses y/o monto) e
inferir el dato faltante, calcular adeudo/saldo al mes actual y
consolidar lo cobrado por el edificio.

Cómo usar
---------
1) Ejecuta el programa y captura:
   - Año actual (AAAA) y mes actual (1..12).
   - N: cuántos contratos vas a registrar.
2) Por inquilino:
   - Nombre y Depto (p.ej. D101).
   - Tipo de depto: 3 o 4 recámaras.
   - Mes/año del último contrato.
   - Si el contrato NO es 2024/2025, captura renta histórica mensual.
   - Pagos del año actual: meses pagados (permite fracciones) y/o monto pagado.
     Si uno de los dos es 0, se infiere a partir del otro.
3) Se mostrará el resumen por inquilino (adeudo/saldo) y al final el total
   cobrado del edificio en el año.

Convenciones y notas
--------------------
- Corte al día 1 de cada mes: meses transcurridos = mes actual (1..12).
- Entradas inválidas se re-preguntan con `continue`.
- Si escribes 'salir' cuando se pide el NOMBRE del inquilino, se usa `break`
  para salir del registro del resto de contratos.
"""

from __future__ import annotations
from dataclasses import dataclass


# =========================
# Utilidades de validación
# =========================

def ask_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Pide un entero con validación de rango. Re-pregunta hasta ser válido (usa `continue`)."""
    while True:
        raw = input(prompt).strip()
        try:
            val = int(raw)
            if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
                print(f"  ⚠️  Debe estar entre {min_val} y {max_val}. Intenta de nuevo.")
                continue
            return val
        except ValueError:
            print("  ⚠️  Ingresa un entero válido.")


def ask_float(prompt: str, min_val: float | None = None) -> float:
    """Pide un número real (float). Re-pregunta hasta ser válido (usa `continue`)."""
    while True:
        raw = input(prompt).strip().replace(",", ".")
        try:
            val = float(raw)
            if min_val is not None and val < min_val:
                print(f"  ⚠️  Debe ser ≥ {min_val}. Intenta de nuevo.")
                continue
            return val
        except ValueError:
            print("  ⚠️  Ingresa un número válido (puede llevar decimales).")


def ask_str(prompt: str) -> str:
    """Pide una cadena no vacía (salvo que el usuario ponga 'salir' para abortar el resto)."""
    while True:
        s = input(prompt).strip()
        if not s:
            print("  ⚠️  No dejes vacío. Intenta de nuevo.")
            continue
        return s


# =========================
# Modelo de dominio (OOP)
# =========================

@dataclass
class BaseContract:
    """Contrato base: datos comunes y utilidades de cálculo."""
    tenant_name: str
    unit_code: str
    start_month: int
    start_year: int
    monthly_rent: float

    def expected_due(self, month_current: int) -> float:
        """Monto debido desde enero hasta month_current (incluyente)."""
        return month_current * self.monthly_rent

    def infer_months_or_amount(self, months_paid: float, amount_paid: float) -> tuple[float, float]:
        """
        Si months_paid == 0 y amount_paid > 0, infiere months_paid = amount_paid / monthly_rent.
        Si amount_paid == 0 y months_paid > 0, infiere amount_paid = months_paid * monthly_rent.
        """
        if months_paid == 0 and amount_paid > 0 and self.monthly_rent > 0:
            months_paid = amount_paid / self.monthly_rent
        if amount_paid == 0 and months_paid > 0:
            amount_paid = months_paid * self.monthly_rent
        return months_paid, amount_paid

    def balance(self, month_current: int, months_paid: float, amount_paid: float) -> tuple[float, float, float]:
        """
        Devuelve (adeudoEsperado, debe, saldoFavor) al mes actual.
        diferencia = amount_paid - adeudoEsperado
          - Si diferencia < 0 => debe = -diferencia, saldoFavor = 0
          - Si diferencia ≥ 0 => debe = 0, saldoFavor = diferencia
        """
        adeudo_esperado = self.expected_due(month_current)
        diferencia = amount_paid - adeudo_esperado
        if diferencia < 0:
            return adeudo_esperado, -diferencia, 0.0
        return adeudo_esperado, 0.0, diferencia


@dataclass
class StandardContract(BaseContract):
    """Contrato vigente 2024–2025. Establece la renta estándar según #recámaras."""
    bedrooms: int = 3

    @staticmethod
    def from_input(tenant_name: str, unit_code: str, start_month: int, start_year: int, bedrooms: int) -> "StandardContract":
        monthly = 7500.0 if bedrooms == 3 else 8500.0
        return StandardContract(
            tenant_name=tenant_name,
            unit_code=unit_code,
            start_month=start_month,
            start_year=start_year,
            monthly_rent=monthly,
            bedrooms=bedrooms,
        )


@dataclass
class HistoricContract(BaseContract):
    """Contrato en prórroga (no vigente 2024–2025). Usa la renta histórica capturada."""
    pass


class BuildingManager:
    """Orquesta la captura de N contratos e imprime resúmenes y total del edificio."""
    def __init__(self, year_current: int, month_current: int):
        self.year_current = year_current
        self.month_current = month_current
        self.total_building = 0.0

    def capture_and_process(self, num_contracts: int) -> None:
        for idx in range(1, num_contracts + 1):
            print("\n---------------------------------------------")
            print(f"Registro #{idx}")

            # Permitir abortar el resto de la sesión con 'salir' → uso de break
            tenant_name = ask_str("Nombre del inquilino (o escribe 'salir' para terminar): ")
            if tenant_name.lower() == "salir":
                print("Cancelaste el resto de la captura. Terminando…")
                break

            unit_code = ask_str("Clave del departamento (ej. D101, D202): ")

            # Validar tipo de depto (3/4) → re-pregunta con continue si inválido
            bedrooms = ask_int("Tipo de departamento (3 = tres recámaras, 4 = cuatro recámaras): ", 3, 4)
            if bedrooms not in (3, 4):
                print("  ⚠️  Tipo inválido (solo 3 o 4). Reiniciando este registro…")
                continue  # <- continue para reiniciar el registro actual

            # Fecha del último contrato
            start_month = ask_int("Mes del último contrato (1..12): ", 1, 12)
            start_year = ask_int("Año del último contrato (AAAA): ")

            # ¿Vigente 2024–2025?
            if 2024 <= start_year <= 2025:
                contract: BaseContract = StandardContract.from_input(
                    tenant_name, unit_code, start_month, start_year, bedrooms
                )
            else:
                print("Contrato no actual (<> 2024-2025).")
                monthly_rent = ask_float("Ingresa la renta mensual estipulada en el contrato: ", min_val=0.0)
                contract = HistoricContract(
                    tenant_name=tenant_name,
                    unit_code=unit_code,
                    start_month=start_month,
                    start_year=start_year,
                    monthly_rent=monthly_rent,
                )

            # Pagos del año en curso
            print(f"Mes actual del sistema: {self.month_current} (enero..{self.month_current})")
            months_paid = ask_float(
                f"Meses pagados en {self.year_current} (permite decimales; si no sabes, ingresa 0): ",
                min_val=0.0,
            )
            amount_paid = ask_float(
                f"Monto pagado en {self.year_current} (si ya indicaste meses, ingresa 0): ",
                min_val=0.0,
            )

            # Inferir el dato faltante (tabla de verdad simple)
            months_paid, amount_paid = contract.infer_months_or_amount(months_paid, amount_paid)

            # Cálculos al corte del mes actual
            expected, due, in_favor = contract.balance(self.month_current, months_paid, amount_paid)
            self.total_building += amount_paid

            # Salida por inquilino
            print("\nResumen")
            print(f"  Inquilino: {tenant_name}  |  Depto: {unit_code}")
            print(f"  Renta mensual: ${contract.monthly_rent:,.2f}")
            print(f"  Meses transcurridos en {self.year_current}: {self.month_current}")
            print(f"  Meses pagados en {self.year_current}: {months_paid:.2f}")
            print(f"  Monto pagado en {self.year_current}: ${amount_paid:,.2f}")
            print(f"  Debió pagar a la fecha: ${expected:,.2f}")
            if due > 0:
                print(f"  * Adeudo actual: ${due:,.2f}")
            if in_favor > 0:
                print(f"  * Saldo a favor: ${in_favor:,.2f}")

    def print_total(self) -> None:
        print("\n=============================================")
        print(f"TOTAL COBRADO EN {self.year_current}: ${self.total_building:,.2f}")
        print("=============================================")


# =========================
# Programa principal
# =========================

def main() -> None:
    print("\n=== Control de Contratos y Pagos — 2025 ===\n")

    year_current = ask_int("Año actual (AAAA): ")
    month_current = ask_int("Mes actual (1..12): ", 1, 12)

    num_contracts = ask_int("¿Cuántos contratos registrarás hoy?: ", 0)
    manager = BuildingManager(year_current, month_current)

    manager.capture_and_process(num_contracts)
    manager.print_total()


if __name__ == "__main__":
    main()