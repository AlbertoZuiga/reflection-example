"""Servicio CRUD para gestionar usuarios en memoria."""

from __future__ import annotations

from typing import List, Optional

from app.models.usuario import Usuario


class UsuarioService:
    """Gestiona las operaciones CRUD de usuarios en memoria.

    Esta clase encapsula toda la lógica de negocio relacionada con
    usuarios, sin preocuparse por la presentación o entrada/salida.
    """

    def __init__(self) -> None:
        """Inicializa el servicio de usuarios."""
        self.usuarios: List[Usuario] = []
        self.siguiente_id: int = 1

    def crear_usuario(self, nombre: str, email: str) -> Usuario:
        """Crea y almacena un usuario nuevo.

        Args:
            nombre: Nombre del usuario.
            email: Correo electrónico del usuario.

        Returns:
            El usuario recién creado.

        Raises:
            ValueError: Si el nombre está vacío o el email es inválido.
        """
        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío.")

        if "@" not in email:
            raise ValueError("Email inválido (debe contener '@').")

        usuario = Usuario(
            usuario_id=self.siguiente_id,
            nombre=nombre,
            email=email,
        )
        self.usuarios.append(usuario)
        self.siguiente_id += 1

        return usuario

    def obtener_todos(self) -> List[Usuario]:
        """Obtiene la lista completa de usuarios.

        Returns:
            Lista de todos los usuarios registrados.
        """
        return self.usuarios.copy()

    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca un usuario por su identificador.

        Args:
            usuario_id: Identificador del usuario.

        Returns:
            El usuario si existe; de lo contrario, None.
        """
        for usuario in self.usuarios:
            if usuario.id == usuario_id:
                return usuario
        return None

    def actualizar_usuario(
        self, usuario_id: int, nombre: Optional[str] = None, email: Optional[str] = None
    ) -> Usuario:
        """Actualiza los datos de un usuario existente.

        Args:
            usuario_id: Identificador del usuario a actualizar.
            nombre: Nuevo nombre (opcional).
            email: Nuevo email (opcional).

        Returns:
            El usuario actualizado.

        Raises:
            ValueError: Si el usuario no existe, o los datos son inválidos.
        """
        usuario = self.obtener_por_id(usuario_id)

        if usuario is None:
            raise ValueError(f"Usuario con ID {usuario_id} no encontrado.")

        if nombre is not None and nombre.strip():
            usuario.nombre = nombre.strip()

        if email is not None:
            if "@" not in email:
                raise ValueError("Email inválido (debe contener '@').")
            usuario.email = email

        return usuario

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """Elimina un usuario del sistema.

        Args:
            usuario_id: Identificador del usuario a eliminar.

        Returns:
            True si se eliminó correctamente; False si no existe.
        """
        usuario = self.obtener_por_id(usuario_id)

        if usuario is None:
            return False

        self.usuarios.remove(usuario)
        return True
