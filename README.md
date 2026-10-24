# vexselector

Listas de selección para terminal. Se elige pulsando la tecla indicada o haciendo clic con el ratón.

```
Selecciona una opción:

[1] Ejecutar app
[2] Ver configuración
[3] Salir
[d] Debug mode
```

## Instalación

```bash
pip install vexselector
```

En Windows, `windows-curses` se instala automáticamente.

## Uso

```python
from vexselector import select, Option

resultado = select("Selecciona una opción:", [
    Option("1", "Ejecutar app"),
    Option("2", "Ver configuración"),
    Option("3", "Salir"),
    Option("d", "Debug mode"),
])

if resultado == "1":
    print("Ejecutando...")
```

Prueba rápida: `python -m vexselector`

## Cómo se elige

- Pulsando la tecla indicada (no distingue mayúsculas).
- Haciendo clic con el ratón sobre el elemento (al pasar por encima se resalta).
- Con ↑/↓ y Enter.
- `Esc` o `Ctrl+C` cancelan y devuelven `None`.

## API

### `Option(key, label, value=None)`

- `key`: tecla de acceso rápido (un carácter).
- `label`: texto mostrado.
- `value`: valor que devuelve `select` al elegirla; si es `None`, devuelve la `key`.

### `select(title, options, default=0)`

Muestra la lista y devuelve el valor de la opción elegida, o `None` si se cancela.
`default` es el índice de la opción resaltada al inicio.

## Notas

- Requiere un terminal con soporte de ratón para los clics (Windows Terminal, iTerm2, GNOME Terminal, etc.).
- Al elegir, la pantalla de la lista se limpia.

## Licencia

MIT
