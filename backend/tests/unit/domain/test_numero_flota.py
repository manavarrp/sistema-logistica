"""
Tests unitarios para el Value Object NumeroFlota.

Cubre:
  - Formatos válidos (AAA1234A)
  - Formatos inválidos (todos los casos de borde)
  - Normalización a mayúsculas
  - Igualdad entre instancias
"""
import pytest
from src.domain.value_objects.numero_flota import NumeroFlota
from src.shared.exceptions import ValidationError


class TestNumeroFlotaValido:

    def test_formato_correcto(self):
        flota = NumeroFlota("ABC1234D")
        assert flota.value == "ABC1234D"

    def test_normaliza_a_mayusculas(self):
        flota = NumeroFlota("abc1234d")
        assert flota.value == "ABC1234D"

    def test_elimina_espacios(self):
        flota = NumeroFlota("  ABC1234D  ")
        assert flota.value == "ABC1234D"

    def test_str_retorna_valor(self):
        assert str(NumeroFlota("XYZ9999Z")) == "XYZ9999Z"

    def test_igualdad_entre_instancias(self):
        assert NumeroFlota("ABC1234D") == NumeroFlota("ABC1234D")

    def test_desigualdad_entre_instancias(self):
        assert NumeroFlota("ABC1234D") != NumeroFlota("XYZ9999Z")

    def test_hashable(self):
        flotas = {NumeroFlota("ABC1234D"), NumeroFlota("XYZ9999Z")}
        assert len(flotas) == 2


class TestNumeroFlotaInvalido:

    @pytest.mark.parametrize("valor_invalido", [
        "AB1234D",    # Solo 2 letras iniciales
        "ABCD1234D",  # 4 letras iniciales
        "ABC123D",    # Solo 3 números
        "ABC12345D",  # 5 números
        "ABC1234",    # Falta letra final
        "1234ABCD",   # Formato invertido
        "ABC1234DD",  # 2 letras al final
        "",           # Vacío
        "ABC123#D",   # Caracter especial
    ])
    def test_rechaza_formato_invalido(self, valor_invalido):
        with pytest.raises(ValidationError) as exc_info:
            NumeroFlota(valor_invalido)
        assert "AAA1234A" in exc_info.value.message