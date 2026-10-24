"""
vexselector - Listas de selección para terminal (teclado + ratón).

Uso:
    from vexselector import select, Option

    resultado = select("Selecciona una opción:", [
        Option("1", "Ejecutar app"),
        Option("2", "Ver configuración"),
        Option("3", "Salir"),
        Option("d", "Debug mode"),
    ])

Se puede elegir:
  - pulsando la tecla indicada ([1], [2], [3], [d]...)
  - haciendo clic con el ratón sobre el elemento
  - con ↑/↓ (o k/j si no son teclas de opción) y Enter

Devuelve el `value` de la opción elegida (o su `key` si no se definió value),
o None si se cancela con Esc / Ctrl+C.

Requisitos:
  - Linux / macOS: nada extra (usa curses de la librería estándar).
  - Windows: windows-curses se instala automáticamente con el paquete.
"""

import curses
import os
from dataclasses import dataclass
from typing import Any, Optional, Sequence

# Evita el retardo al pulsar Esc en curses
os.environ.setdefault("ESCDELAY", "25")


@dataclass
class Option:
    key: str            # tecla de acceso rápido (un carácter)
    label: str          # texto mostrado
    value: Any = None   # valor devuelto (por defecto, la key)

    def __post_init__(self):
        if len(self.key) != 1:
            raise ValueError(f"La tecla debe ser un solo carácter: {self.key!r}")

    @property
    def text(self) -> str:
        return f"[{self.key}] {self.label}"

    @property
    def result(self) -> Any:
        return self.key if self.value is None else self.value


def _loop(stdscr, title: str, options: Sequence[Option], default: int):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.mouseinterval(0)

    use_colors = curses.has_colors()
    if use_colors:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_CYAN)
    highlight_attr = curses.color_pair(1) if use_colors else curses.A_REVERSE

    keys = {o.key.lower(): i for i, o in enumerate(options)}
    current = default
    top = 2  # fila donde empieza la primera opción

    click_mask = (
        curses.BUTTON1_PRESSED | curses.BUTTON1_CLICKED | curses.BUTTON1_RELEASED
    )

    def item_at(y: int, x: int) -> Optional[int]:
        i = y - top
        if 0 <= i < len(options) and 0 <= x < len(options[i].text):
            return i
        return None

    while True:
        stdscr.erase()
        try:
            stdscr.addstr(0, 0, title, curses.A_BOLD)
            for i, opt in enumerate(options):
                attr = highlight_attr if i == current else curses.A_NORMAL
                stdscr.addstr(top + i, 0, opt.text, attr)
        except curses.error:
            pass  # terminal demasiado pequeña
        stdscr.refresh()

        ch = stdscr.getch()

        if ch == curses.KEY_MOUSE:
            try:
                _, mx, my, _, bstate = curses.getmouse()
            except curses.error:
                continue
            idx = item_at(my, mx)
            if idx is None:
                continue
            if bstate & click_mask:
                return options[idx].result
            current = idx  # hover: solo resalta
        elif ch in (curses.KEY_UP,):
            current = (current - 1) % len(options)
        elif ch in (curses.KEY_DOWN,):
            current = (current + 1) % len(options)
        elif ch in (curses.KEY_ENTER, 10, 13):
            return options[current].result
        elif ch == 27:  # Esc
            return None
        elif 0 <= ch < 256:
            c = chr(ch).lower()
            if c in keys:
                return options[keys[c]].result
            if c == "k":
                current = (current - 1) % len(options)
            elif c == "j":
                current = (current + 1) % len(options)


def select(title: str, options: Sequence[Option], default: int = 0) -> Any:
    """Muestra la lista y devuelve el valor de la opción elegida (o None)."""
    if not options:
        raise ValueError("Se necesita al menos una opción")
    try:
        return curses.wrapper(_loop, title, list(options), default)
    except KeyboardInterrupt:
        return None


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
