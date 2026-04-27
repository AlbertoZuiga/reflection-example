# CRUD de usuarios con reflection en Python

Proyecto didáctico: un CRUD de usuarios en consola que usa introspección (reflection)
para construir su menú dinámico. El programa busca automáticamente los métodos que
comienzan con `op_` y los convierte en opciones numeradas.

Ideal para entender cómo detectar y ejecutar operaciones dinámicamente sin base de datos.

## ¿Qué es reflection en Python?

Reflection (introspección) permite que un programa inspeccione objetos en tiempo de ejecución. En
Python se usan funciones como `dir()`, `inspect` y `getattr()` para:

- Enumerar métodos y atributos
- Obtener referencias a funciones por nombre
- Ejecutar funciones dinámicamente

En este proyecto, `MenuReflection` detecta métodos que empiezan con `op_` y arma el menú.

## Estructura del proyecto (refactorizado)

```text
reflection/
├── app/
│   ├── core/
│   │   └── menu.py              # Lógica de reflection y menú dinámico
│   ├── operations/
│   │   ├── sistema_operaciones.py # op_salir y control general
│   │   └── usuario_operaciones.py # op_crear_usuario, op_listar_usuarios, etc.
│   ├── models/
│   │   └── usuario.py           # Modelo de datos (Usuario)
│   ├── services/
│   │   └── usuario_service.py   # Servicio CRUD (lógica de negocio)
│   ├── ui/
│   │   └── consola.py           # Interfaz de consola (Rich)
│   └── app.py      # Orquestador mínimo
├── main.py
├── requirements.txt
└── README.md
```

## Componentes principales

- `main.py`: punto de entrada; crea `App` y arranca el menú.
- `app/app.py`: orquestador que coordina servicios, UI y operaciones.
- `app/operations/usuario_operaciones.py`: contiene las operaciones `op_*` del CRUD.
- `app/operations/sistema_operaciones.py`: operaciones del sistema (por ejemplo `op_salir`).
- `app/core/menu.py`: núcleo de reflection que detecta y ejecuta operaciones.
- `app/models/usuario.py`: modelo `Usuario` con `id`, `nombre`, `email`.
- `app/services/usuario_service.py`: lógica CRUD independiente de la UI.
- `app/ui/consola.py`: presentación e interacción con `rich`.

## Cómo funciona el menú dinámico

1. `App` crea objetos de operaciones.
2. `MenuReflection` inspecciona esos objetos y detecta métodos con prefijo `op_`.
3. El menú se construye a partir de esa lista y muestra opciones numeradas.
4. La opción elegida se ejecuta dinámicamente con `getattr()`.

## Beneficios de la refactorización

- Separación de responsabilidades: modelos, servicios, UI y core independientes.
- Mantenibilidad y escalabilidad: fácil añadir persistencia o una API.

## Requisitos

- Python 3.12 o superior
- `pip` para instalar dependencias

## Instalación y ejecución

Clonar repositorio

```bash
git clone https://github.com/AlbertoZuiga/reflection-example
cd reflection-example
```

Crear y activar entorno virtual de python

```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En macOS / Linux:
source .venv/bin/activate

# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# En Windows (CMD):
.venv\Scripts\activate.bat
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Ejecutar la aplicación:

```bash
python main.py
```

## Añadir nuevas operaciones

Solo crea un método que empiece con `op_` en la clase de operaciones correspondiente. El menú
lo descubrirá automáticamente en la siguiente ejecución.

Ejemplo:

```python
def op_buscar_por_email(self) -> None:
    """Busca usuarios en memoria a partir de su email."""
    email = Prompt.ask("Email a buscar").strip()
    encontrados = [u for u in self.servicio.obtener_todos() if u.email == email]

    if not encontrados:
        self.consola.mostrar_error("No se encontraron usuarios.")
        return

    self.consola.mostrar_tabla_usuarios(encontrados)
```

## Notas para principiantes

- Los datos se guardan en memoria y se pierden al cerrar el programa.
- `rich` se usa para mejorar la presentación en consola.
- El prefijo `op_` indica qué métodos aparecen automáticamente en el menú.
