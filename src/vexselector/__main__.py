from . import Option, select

if __name__ == "__main__":
    elegido = select(
        "Selecciona una opción:",
        [
            Option("1", "Ejecutar app"),
            Option("2", "Ver configuración"),
            Option("3", "Salir"),
            Option("d", "Debug mode"),
        ],
    )
    print(f"Elegiste: {elegido!r}")
