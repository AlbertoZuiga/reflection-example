"""
Ejemplo didáctico de reflection (introspección) en Python.

Este programa construye un menú dinámico en consola para un CRUD de usuarios.
Las opciones del menú se descubren automáticamente buscando métodos con prefijo "op_".

Estructura refactorizada:
- models: Definen la estructura de datos (Usuario)
- services: Contienen la lógica de negocio (CRUD)
- operations: Contienen las operaciones `op_*` del menú
- ui: Gestiona la presentación e interacción
- core: Implementa la reflection y el menú dinámico
- sistema_usuarios: Orquesta los componentes
"""

from __future__ import annotations

from app.core.menu import MenuReflection
from app.operations import SistemaOperaciones, UsuarioOperaciones
from app.services.usuario_service import UsuarioService
from app.ui.consola import Consola


class App:
    """Orquestador principal del sistema CRUD de usuarios.

    Esta clase coordina la interacción entre:
    - La capa de presentación (Consola)
    - La capa de reflection (MenuReflection)

    El menú se construye dinámicamente detectando métodos con prefijo "op_",
    que se ejecutan de forma automática sin necesidad de if/match explícitos.
    """

    def __init__(self) -> None:
        """Inicializa el sistema con sus componentes."""
        self.consola = Consola()
        self.operaciones_usuario = UsuarioOperaciones(self.consola, UsuarioService())
        self.operaciones_sistema = SistemaOperaciones(self.consola, self._detener)
        self.menu = MenuReflection(
            [self.operaciones_usuario, self.operaciones_sistema], prefijo="op_"
        )
        self.en_ejecucion: bool = True

    def ejecutar(self) -> None:
        """Ejecuta el bucle principal e interactúa con el usuario.

        El menú se construye en cada iteración a partir de los métodos ``op_``.
        Al usar ``getattr`` sobre el nombre elegido, la acción se invoca de forma
        dinámica sin necesidad de un ``if`` o ``match`` por cada opción.
        """
        while self.en_ejecucion:
            # Reflection para detectar operaciones disponibles
            operaciones = self.menu.obtener_todas_operaciones()

            # Presentación del menú
            self.consola.mostrar_header()
            self.consola.mostrar_opciones_menu(operaciones)

            # Obtener selección del usuario
            seleccion = self.consola.solicitar_opcion()

            # Validación de entrada
            if not self.menu.validar_seleccion(seleccion, len(operaciones)):
                self.consola.mostrar_error("Debes ingresar un numero de opcion valido.")
                continue

            # Obtener y ejecutar la operación seleccionada
            indice = self.menu.obtener_indice_operacion(seleccion)
            operacion = self.menu.obtener_operacion_por_indice(operaciones, indice)

            # Reflection real de ejecución: getattr + invocación dinámica
            self.menu.ejecutar_operacion(operacion)

            if operacion.nombre != "op_salir":
                self.consola.pausar_continuar()

    def _detener(self) -> None:
        """Marca el sistema para finalizar el bucle principal."""
        self.en_ejecucion = False
