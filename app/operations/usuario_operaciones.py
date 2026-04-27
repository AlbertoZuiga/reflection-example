"""Operaciones de usuario expuestas al menú dinámico."""

from __future__ import annotations

from app.services.usuario_service import UsuarioService
from app.ui.consola import Consola


class UsuarioOperaciones:
    """Agrupa las operaciones `op_*` relacionadas con usuarios."""

    def __init__(self, consola: Consola, servicio: UsuarioService) -> None:
        self.consola = consola
        self.servicio = servicio

    def op_crear_usuario(self) -> None:
        """Solicita datos y agrega un usuario nuevo al servicio."""
        self.consola.mostrar_header_seccion("Crear Usuario")

        nombre = self.consola.solicitar_texto("Nombre")
        email = self.consola.solicitar_texto("Email")

        try:
            usuario = self.servicio.crear_usuario(nombre, email)
            self.consola.mostrar_exito(f"Usuario creado con id={usuario.id}.")
        except ValueError as e:
            self.consola.mostrar_error(str(e))

    def op_listar_usuarios(self) -> None:
        """Muestra en pantalla la lista de usuarios registrados en formato tabla."""
        self.consola.mostrar_header_seccion("Listar Usuarios")
        usuarios = self.servicio.obtener_todos()
        self.consola.mostrar_tabla_usuarios(usuarios)

    def op_actualizar_usuario(self) -> None:
        """Permite modificar el nombre y el email de un usuario existente."""
        self.consola.mostrar_header_seccion("Actualizar Usuario")

        dato_id = self.consola.solicitar_texto("ID del usuario a actualizar")

        if not dato_id.isdigit():
            self.consola.mostrar_error("El ID debe ser numerico.")
            return

        usuario_id = int(dato_id)
        usuario = self.servicio.obtener_por_id(usuario_id)

        if usuario is None:
            self.consola.mostrar_error("Usuario no encontrado.")
            return

        nuevo_nombre = self.consola.solicitar_texto(
            f"Nuevo nombre ({usuario.nombre})", default=usuario.nombre
        )
        nuevo_email = self.consola.solicitar_texto(
            f"Nuevo email ({usuario.email})", default=usuario.email
        )

        try:
            self.servicio.actualizar_usuario(usuario_id, nuevo_nombre, nuevo_email)
            self.consola.mostrar_exito("Usuario actualizado correctamente.")
        except ValueError as e:
            self.consola.mostrar_advertencia(
                f"{str(e)} Se mantienen los datos anteriores."
            )

    def op_eliminar_usuario(self) -> None:
        """Elimina del servicio al usuario indicado por su identificador."""
        self.consola.mostrar_header_seccion("Eliminar Usuario")

        dato_id = self.consola.solicitar_texto("ID del usuario a eliminar")

        if not dato_id.isdigit():
            self.consola.mostrar_error("El ID debe ser numerico.")
            return

        usuario_id = int(dato_id)

        if self.servicio.eliminar_usuario(usuario_id):
            self.consola.mostrar_exito("Usuario eliminado correctamente.")
        else:
            self.consola.mostrar_error("Usuario no encontrado.")
