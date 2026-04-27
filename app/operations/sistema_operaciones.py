"""Operaciones del sistema que no pertenecen al dominio de usuario."""

from __future__ import annotations

from typing import Callable

from app.ui.consola import Consola


class SistemaOperaciones:
    """Agrupa operaciones de control general del sistema."""

    def __init__(self, consola: Consola, detener_sistema: Callable[[], None]) -> None:
        self.consola = consola
        self.detener_sistema = detener_sistema

    def op_salir(self) -> None:
        """Finaliza el bucle principal del programa."""
        self.consola.mostrar_salida()
        self.detener_sistema()
