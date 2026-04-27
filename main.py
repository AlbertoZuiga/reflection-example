"""Punto de entrada principal del CRUD de usuarios."""

from app.app import App


def main() -> None:
    """Crea la aplicacion y arranca el menu interactivo."""
    sistema = App()
    sistema.ejecutar()


if __name__ == "__main__":
    main()
