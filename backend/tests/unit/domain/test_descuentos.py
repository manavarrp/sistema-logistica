"""
Tests unitarios para las reglas de descuento por volumen.

Reglas de negocio verificadas:
  - Terrestre: 5% de descuento si cantidad > 10
  - Marítimo:  3% de descuento si cantidad > 10
  - Sin descuento si cantidad <= 10
  - El umbral es estrictamente mayor a 10 (no >=)
"""
import pytest
from decimal import Decimal
from src.domain.rules.descuentos import (
    calcular_descuento_terrestre,
    calcular_descuento_maritimo,
)


class TestDescuentoTerrestre:
    """Regla: cantidad > 10 → 5% del subtotal."""

    def test_sin_descuento_cantidad_igual_a_10(self):
        subtotal = Decimal("1000.00")
        descuento = calcular_descuento_terrestre(cantidad=10, subtotal=subtotal)
        assert descuento == Decimal("0")

    def test_sin_descuento_cantidad_menor_a_10(self):
        subtotal = Decimal("500.00")
        descuento = calcular_descuento_terrestre(cantidad=5, subtotal=subtotal)
        assert descuento == Decimal("0")

    def test_sin_descuento_cantidad_1(self):
        subtotal = Decimal("50000.00")
        descuento = calcular_descuento_terrestre(cantidad=1, subtotal=subtotal)
        assert descuento == Decimal("0")

    def test_descuento_5_porciento_cantidad_11(self):
        """El umbral es estrictamente > 10, no >= 10."""
        subtotal = Decimal("1000.00")
        descuento = calcular_descuento_terrestre(cantidad=11, subtotal=subtotal)
        assert descuento == Decimal("50.00")

    def test_descuento_5_porciento_cantidad_15(self):
        subtotal = Decimal("750000.00")
        descuento = calcular_descuento_terrestre(cantidad=15, subtotal=subtotal)
        assert descuento == Decimal("37500.00")

    def test_descuento_5_porciento_cantidad_100(self):
        subtotal = Decimal("5000000.00")
        descuento = calcular_descuento_terrestre(cantidad=100, subtotal=subtotal)
        assert descuento == Decimal("250000.00")

    def test_descuento_con_precio_decimal(self):
        """Verifica precisión decimal en el cálculo."""
        subtotal = Decimal("333.33")
        descuento = calcular_descuento_terrestre(cantidad=20, subtotal=subtotal)
        assert descuento == Decimal("333.33") * Decimal("0.05")

    def test_retorna_decimal(self):
        """El tipo de retorno debe ser Decimal para mantener precisión."""
        resultado = calcular_descuento_terrestre(5, Decimal("100"))
        assert isinstance(resultado, Decimal)


class TestDescuentoMaritimo:
    """Regla: cantidad > 10 → 3% del subtotal."""

    def test_sin_descuento_cantidad_igual_a_10(self):
        subtotal = Decimal("1000.00")
        descuento = calcular_descuento_maritimo(cantidad=10, subtotal=subtotal)
        assert descuento == Decimal("0")

    def test_sin_descuento_cantidad_menor_a_10(self):
        subtotal = Decimal("850000.00")
        descuento = calcular_descuento_maritimo(cantidad=3, subtotal=subtotal)
        assert descuento == Decimal("0")

    def test_descuento_3_porciento_cantidad_11(self):
        subtotal = Decimal("1000.00")
        descuento = calcular_descuento_maritimo(cantidad=11, subtotal=subtotal)
        assert descuento == Decimal("30.00")

    def test_descuento_3_porciento_cantidad_12(self):
        subtotal = Decimal("10200000.00")  # 12 × 850,000
        descuento = calcular_descuento_maritimo(cantidad=12, subtotal=subtotal)
        assert descuento == Decimal("306000.00")

    def test_descuento_menor_que_terrestre(self):
        """El descuento marítimo (3%) siempre es menor que el terrestre (5%)."""
        subtotal = Decimal("1000.00")
        cantidad = 15
        desc_terre = calcular_descuento_terrestre(cantidad, subtotal)
        desc_mari = calcular_descuento_maritimo(cantidad, subtotal)
        assert desc_mari < desc_terre

    def test_retorna_decimal(self):
        resultado = calcular_descuento_maritimo(5, Decimal("100"))
        assert isinstance(resultado, Decimal)


class TestUmbralDescuento:
    """Verifica que el umbral es estrictamente > 10 en ambas reglas."""

    @pytest.mark.parametrize("cantidad, esperado_terre, esperado_mari", [
        (9,  Decimal("0"),     Decimal("0")),
        (10, Decimal("0"),     Decimal("0")),
        (11, Decimal("50.00"), Decimal("30.00")),
        (12, Decimal("50.00"), Decimal("30.00")),
    ])
    def test_umbral_exacto(self, cantidad, esperado_terre, esperado_mari):
        subtotal = Decimal("1000.00")
        assert calcular_descuento_terrestre(cantidad, subtotal) == esperado_terre
        assert calcular_descuento_maritimo(cantidad, subtotal) == esperado_mari