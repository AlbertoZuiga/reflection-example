"""Lógica de reflection para construcción dinámica del menú."""

from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Callable, List, Sequence


@dataclass(frozen=True)
class OperacionMenu:
    """Describe una operación descubierta por reflection."""

    nombre: str
    etiqueta: str
    accion: Callable[[], None]
    origen: str


class MenuReflection:
    """Gestiona la detección dinámica de operaciones mediante reflection.

    La clase inspecciona uno o varios objetos y descubre métodos que comienzan
    con un prefijo específico. Luego permite ejecutar la operación elegida sin
    registrarla manualmente.
    """

    def __init__(
        self, objetos: object | Sequence[object], prefijo: str = "op_"
    ) -> None:
        """Inicializa el manejador de menú con reflection.

        Args:
            objetos: Uno o varios objetos en los que se buscarán métodos.
            prefijo: Prefijo que deben tener los métodos (por defecto "op_").
        """
        if isinstance(objetos, Sequence) and not isinstance(objetos, (str, bytes)):
            self.objetos = tuple(objetos)
        else:
            self.objetos = (objetos,)
        self.prefijo = prefijo

    def obtener_todas_operaciones(self) -> List[OperacionMenu]:
        """Obtiene la lista de operaciones disponibles desde todos los objetos."""
        operaciones: List[OperacionMenu] = []
        for objeto in self.objetos:
            for nombre, metodo in inspect.getmembers(
                objeto, predicate=inspect.ismethod
            ):
                if nombre.startswith(self.prefijo):
                    operaciones.append(
                        OperacionMenu(
                            nombre=nombre,
                            etiqueta=self._texto_opcion(nombre),
                            accion=metodo,
                            origen=objeto.__class__.__name__,
                        )
                    )
        return sorted(
            operaciones,
            key=lambda operacion: (
                self._clave_orden_operacion(operacion.nombre),
                operacion.origen,
            ),
        )

    def ejecutar_operacion(self, operacion: OperacionMenu) -> None:
        """Ejecuta dinámicamente la operación indicada."""
        operacion.accion()

    def validar_seleccion(self, seleccion: str, cantidad_opciones: int) -> bool:
        """Valida que la selección sea un número válido.

        Args:
            seleccion: Texto ingresado por el usuario.
            cantidad_opciones: Cantidad total de opciones disponibles.

        Returns:
            True si la selección es válida; False en caso contrario.
        """
        if not seleccion.isdigit():
            return False

        indice = int(seleccion)
        return 1 <= indice <= cantidad_opciones

    def obtener_indice_operacion(self, seleccion: str) -> int:
        """Convierte la selección del usuario en un índice de operación.

        Args:
            seleccion: Número ingresado por el usuario (1-based).

        Returns:
            Índice de la operación (0-based).
        """
        return int(seleccion) - 1

    def obtener_operacion_por_indice(
        self, operaciones: List[OperacionMenu], indice: int
    ) -> OperacionMenu:
        """Obtiene la operación a partir del índice seleccionado."""
        return operaciones[indice]

    @staticmethod
    def _texto_opcion(nombre_metodo: str) -> str:
        """Convierte el nombre de un método en una etiqueta legible."""
        return nombre_metodo.replace("op_", "", 1).replace("_", " ").title()

    def _clave_orden_operacion(self, nombre_metodo: str) -> tuple[int, str]:
        """Ordena las operaciones dejando `op_salir` siempre al final."""
        return (1, nombre_metodo) if nombre_metodo == f"{self.prefijo}salir" else (0, nombre_metodo)
