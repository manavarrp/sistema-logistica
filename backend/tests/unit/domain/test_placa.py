"""
Tests unitarios para el Value Object Placa.

Cubre:
  - Formatos válidos
  - Formatos inválidos (todos los casos de borde)
  - Normalización a mayúsculas
  - Igualdad entre instancias
"""
import pytest
from src.domain.value_objects.placa import Placa
from src.shared.exceptions import ValidationError


class TestPlacaValida:
    """El Value Object debe aceptar cualquier placa con formato AAA123."""

    def test_formato_correcto(self):
        placa = Placa("ABC123")
        assert placa.value == "ABC123"

    def test_normaliza_a_mayusculas(self):
        placa = Placa("abc123")
        assert placa.value == "ABC123"

    def test_elimina_espacios(self):
        placa = Placa("  ABC123  ")
        assert placa.value == "ABC123"

    def test_str_retorna_valor(self):
        assert str(Placa("XYZ999")) == "XYZ999"

    def test_igualdad_entre_instancias(self):
        assert Placa("ABC123") == Placa("ABC123")

    def test_desigualdad_entre_instancias(self):
        assert Placa("ABC123") != Placa("XYZ999")

    def test_hashable(self):
        """Debe poder usarse como clave en sets y dicts."""
        placas = {Placa("ABC123"), Placa("XYZ999")}
        assert len(placas) == 2


class TestPlacaInvalida:
    """El Value Object debe rechazar cualquier formato incorrecto."""

    @pytest.mark.parametrize("valor_invalido", [
        "AB123",      # Solo 2 letras
        "ABCD123",    # 4 letras
        "ABC12",      # Solo 2 números
        "ABC1234",    # 4 números
        "123ABC",     # Números primero
        "A1B2C3",     # Alternado
        "ABC 123",    # Con espacio interno
        "",           # Vacío
        "ABC12#",     # Caracter especial
        "abc12!",     # Caracter especial minúscula
    ])
    def test_rechaza_formato_invalido(self, valor_invalido):
        with pytest.raises(ValidationError) as exc_info:
            Placa(valor_invalido)
        assert "AAA123" in exc_info.value.message