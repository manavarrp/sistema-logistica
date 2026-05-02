"""
Excepciones personalizadas del dominio.
Permite distinguir errores de negocio de errores técnicos.
"""


class DomainException(Exception):
    """Base de todas las excepciones del dominio."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ValidationError(DomainException):
    """Validación de formato o regla de negocio fallida."""
    pass


class NotFoundError(DomainException):
    """Entidad no encontrada en base de datos."""
    pass


class DuplicateError(DomainException):
    """Violación de unicidad."""
    pass


class BusinessRuleError(DomainException):
    """Regla de negocio violada."""
    pass