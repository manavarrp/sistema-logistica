"""Value Object: NumeroFlota - Formato AAA1234A"""
import re
from src.shared.exceptions import ValidationError

PATTERN = re.compile(r'^[A-Z]{3}[0-9]{4}[A-Z]$')


class NumeroFlota:
    def __init__(self, value: str):
        self._value = value.upper().strip()
        if not PATTERN.match(self._value):
            raise ValidationError(f"Número de flota inválido '{self._value}'. Formato esperado: AAA1234A")

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, NumeroFlota) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)