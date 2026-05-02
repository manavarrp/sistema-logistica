"""Value Object: NumeroGuia - 10 caracteres alfanuméricos"""
import re
from src.shared.exceptions import ValidationError

PATTERN = re.compile(r'^[A-Z0-9]{10}$')


class NumeroGuia:
    def __init__(self, value: str):
        self._value = value.upper().strip()
        if not PATTERN.match(self._value):
            raise ValidationError(
                f"Número de guía inválido '{self._value}'. "
                "Debe tener exactamente 10 caracteres alfanuméricos."
            )

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other) -> bool:
        return isinstance(other, NumeroGuia) and self._value == other._value

    def __hash__(self) -> int:
        return hash(self._value)