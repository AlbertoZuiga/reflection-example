"""Modelo de datos para un usuario del sistema."""

from __future__ import annotations


class Usuario:
    """Representa un usuario en el sistema.

    Attributes:
        id: Identificador único del usuario.
        nombre: Nombre completo del usuario.
        email: Correo electrónico del usuario.
    """

    def __init__(self, usuario_id: int, nombre: str, email: str) -> None:
        """Inicializa un usuario nuevo.

        Args:
            usuario_id: Identificador único.
            nombre: Nombre del usuario.
            email: Correo electrónico.
        """
        self.id = usuario_id
        self.nombre = nombre
        self.email = email



    def __repr__(self) -> str:
        """Representación en string del usuario."""
        return f"Usuario(id={self.id}, nombre='{self.nombre}', email='{self.email}')"
