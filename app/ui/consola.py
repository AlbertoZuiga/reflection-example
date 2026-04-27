"""Componente de interfaz de consola con Rich."""

from __future__ import annotations

from typing import List

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from app.core.menu import OperacionMenu
from app.models.usuario import Usuario


class Consola:
    """Gestiona la presentación e interacción con el usuario a través de la consola.

    Esta clase encapsula toda la lógica de entrada/salida (I/O), utilizando Rich
    para mejorar la experiencia visual. La lógica de negocio se mantiene separada.
    """

    def __init__(self) -> None:
        """Inicializa la consola."""
        self.console = Console()

    def mostrar_header(self) -> None:
        """Muestra el encabezado del menú principal."""
        self.console.print()
        self.console.print(
            Panel.fit(
                "[bold cyan]MENU DINAMICO[/bold cyan]\n"
                "[white]Reflection / Introspeccion con [bold]dir[/bold],"
                "[bold]inspect[/bold] y [bold]getattr[/bold][/white]",
                border_style="cyan",
                title="[bold]CRUD Usuarios[/bold]",
            )
        )

    def mostrar_opciones_menu(self, operaciones: List[OperacionMenu]) -> None:
        """Muestra las opciones del menú numeradas.

        Args:
            operaciones: Lista de operaciones detectadas por reflection.
        """
        for indice, operacion in enumerate(operaciones, start=1):
            self.console.print(
                f"[bold blue]{indice}.[/bold blue] [white]{operacion.etiqueta}[/white]"
            )

    def solicitar_opcion(self) -> str:
        """Solicita al usuario que seleccione una opción.

        Returns:
            La entrada del usuario sin espacios al inicio/final.
        """
        return Prompt.ask("[bold]Selecciona una opcion[/bold]").strip()

    def mostrar_error(self, mensaje: str) -> None:
        """Muestra un mensaje de error al usuario.

        Args:
            mensaje: Texto del error.
        """
        self.console.print(f"[bold red]Error:[/bold red] {mensaje}")

    def mostrar_advertencia(self, mensaje: str) -> None:
        """Muestra un mensaje de advertencia al usuario.

        Args:
            mensaje: Texto de la advertencia.
        """
        self.console.print(f"[bold yellow]Advertencia:[/bold yellow] {mensaje}")

    def mostrar_exito(self, mensaje: str) -> None:
        """Muestra un mensaje de éxito al usuario.

        Args:
            mensaje: Texto del éxito.
        """
        self.console.print(f"[bold green]Exito:[/bold green] {mensaje}")



    def mostrar_header_seccion(self, titulo: str) -> None:
        """Muestra el encabezado de una sección/operación.

        Args:
            titulo: Nombre de la sección.
        """
        self.console.print(f"\n[bold cyan][{titulo}][/bold cyan]")

    def solicitar_texto(self, prompt: str, default: str = "") -> str:
        """Solicita al usuario que ingrese un texto.

        Args:
            prompt: Texto de la pregunta.
            default: Valor por defecto (opcional).

        Returns:
            El texto ingresado por el usuario.
        """
        if default:
            return Prompt.ask(prompt, default=default).strip()
        return Prompt.ask(prompt).strip()

    def mostrar_tabla_usuarios(self, usuarios: List[Usuario]) -> None:
        """Muestra una tabla con los datos de usuarios.

        Args:
            usuarios: Lista de usuarios a mostrar.
        """
        if not usuarios:
            self.mostrar_advertencia("No hay usuarios registrados.")
            return

        tabla = Table(title="Usuarios Registrados", header_style="bold cyan")
        tabla.add_column("ID", style="bold", justify="right")
        tabla.add_column("Nombre")
        tabla.add_column("Email")

        for usuario in usuarios:
            tabla.add_row(str(usuario.id), usuario.nombre, usuario.email)

        self.console.print(tabla)

    def mostrar_salida(self) -> None:
        """Muestra el mensaje de salida del sistema."""
        self.console.print("\n[bold yellow]Saliendo del sistema...[/bold yellow]")

    def pausar_continuar(self) -> None:
        """Espera una confirmación del usuario antes de volver al menú."""
        self.console.input("[dim]Presiona ENTER para continuar...[/dim]")
