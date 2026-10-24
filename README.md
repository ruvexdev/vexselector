<div align="center">

# vexselector

**Interactive terminal menus you can drive with a hotkey or a mouse click.**

[![PyPI version](https://img.shields.io/pypi/v/vexselector.svg)](https://pypi.org/project/vexselector/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://pypi.org/project/vexselector/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](#compatibility)

</div>

```
Select an option:

[1] Run app
[2] View settings
[3] Quit
[d] Debug mode
```

`vexselector` is a small, dependency-light Python module for building selection lists in the terminal. Each entry has a hotkey, and every entry is also clickable with the mouse. It is built on the standard-library `curses` module, so there is nothing heavy to install.

## Features

- **Hotkeys**: press the key shown in brackets to choose instantly (case-insensitive).
- **Mouse support**: click any entry to select it; hovering highlights it.
- **Keyboard navigation**: arrow keys and `Enter`, plus `j`/`k` as Vim-style shortcuts.
- **Flexible return values**: get back the option's key, or any Python object you attach to it (strings, enums, functions…).
- **Safe cancellation**: `Esc` or `Ctrl+C` returns `None` instead of raising.
- **Cross-platform**: Windows, Linux and macOS. On Windows, `windows-curses` is installed automatically.
- **Zero configuration**: one function call, no setup, no global state.
- **Typed**: ships with a `py.typed` marker.

## Installation

```bash
pip install vexselector
```

Requires Python 3.8 or newer.

## Quick start

```python
from vexselector import select, Option

choice = select("Select an option:", [
    Option("1", "Run app"),
    Option("2", "View settings"),
    Option("3", "Quit"),
    Option("d", "Debug mode"),
])

if choice == "1":
    print("Running...")
```

Try the built-in demo without writing any code:

```bash
python -m vexselector
```

## Controls

| Input                          | Action                                       |
| ------------------------------ | -------------------------------------------- |
| Option key (e.g. `1`, `d`)     | Select that option immediately               |
| Left mouse click on an entry   | Select that option                           |
| Mouse hover                    | Highlight the entry under the cursor         |
| `↑` / `↓`                      | Move the highlight                           |
| `k` / `j`                      | Move up / down (only if not used as a hotkey)|
| `Enter`                        | Select the highlighted option                |
| `Esc` or `Ctrl+C`              | Cancel and return `None`                     |

## Usage examples

### Returning custom values

Attach any object to an option with `value`. If you leave it out, `select` returns the option's key.

```python
import sys
from vexselector import select, Option

action = select("What now?", [
    Option("r", "Run", value=lambda: print("Running...")),
    Option("q", "Quit", value=sys.exit),
])

if action:          # None means the user cancelled
    action()
```

### A menu loop

```python
from vexselector import select, Option

OPTIONS = [
    Option("1", "Run app", value="run"),
    Option("2", "View settings", value="settings"),
    Option("3", "Quit", value="quit"),
]

while True:
    choice = select("Main menu:", OPTIONS)

    if choice in (None, "quit"):
        break
    elif choice == "run":
        print("Running app...")
    elif choice == "settings":
        print("Showing settings...")
```

### Choosing the initial highlight

`default` is the zero-based index of the entry highlighted when the menu opens, which is what `Enter` will pick if the user doesn't move.

```python
select("Continue?", [Option("y", "Yes"), Option("n", "No")], default=1)
```

## API reference

### `Option(key, label, value=None)`

A single menu entry, rendered as `[key] label`.

| Parameter | Type  | Description                                                                  |
| --------- | ----- | ---------------------------------------------------------------------------- |
| `key`     | `str` | Hotkey. Must be exactly one character and should be unique within a menu.    |
| `label`   | `str` | Text displayed next to the key.                                              |
| `value`   | `Any` | Object returned when chosen. If `None`, the `key` is returned instead.       |

Raises `ValueError` if `key` is not a single character.

### `select(title, options, default=0)`

Displays the menu and blocks until the user chooses or cancels.

| Parameter | Type               | Description                                  |
| --------- | ------------------ | -------------------------------------------- |
| `title`   | `str`              | Heading shown above the list.                |
| `options` | `Sequence[Option]` | The entries to display (at least one).       |
| `default` | `int`              | Index of the initially highlighted entry.    |

**Returns** the chosen option's `value` (or `key`), or `None` if cancelled.

Raises `ValueError` if `options` is empty.

## Compatibility

| Platform | Notes                                                              |
| -------- | ------------------------------------------------------------------ |
| Linux    | Works out of the box.                                              |
| macOS    | Works out of the box.                                              |
| Windows  | Uses `windows-curses`, installed automatically as a dependency.    |

- Mouse clicks require a terminal that reports mouse events (Windows Terminal, iTerm2, GNOME Terminal and most modern emulators). Where unsupported, hotkeys and arrow keys still work.
- `select` needs an interactive terminal (a TTY). It is not intended for piped or non-interactive output.

## Behavior notes

- The menu is drawn on the terminal's alternate screen and cleared once you choose, so the list does not remain visible afterwards. Print your own confirmation if you want a trace.
- The `Esc` key responds quickly: the module sets `ESCDELAY` to `25` ms unless you've already defined it in your environment.

## Development

```bash
git clone https://github.com/YOUR_USERNAME/vexselector.git
cd vexselector
pip install -e .
python -m vexselector
```

Build and validate a release:

```bash
pip install build twine
python -m build
python -m twine check dist/*
```

## Contributing

Issues and pull requests are welcome. For larger changes, please open an issue first to discuss what you'd like to change.

## License

Released under the [MIT License](LICENSE).
