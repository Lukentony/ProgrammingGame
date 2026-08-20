# ProgrammingGame

A small desktop game built with [pygame](https://www.pygame.org/) that teaches basic Python
syntax through short exercises. The in-game text is in Italian (window title: "Impara la
Programmazione" — "Learn Programming").

The player enters their name, then works through a fixed sequence of levels defined in
`levels.json`. Each level shows an instruction (e.g. "create a variable `x` with value 5") and
the player types the matching Python statement into an on-screen input box, either with the
keyboard or an optional on-screen virtual keyboard, and submits it with an Enter button. The
input is checked against a list of accepted answer strings for that level; a correct answer
advances to a congratulations screen and the next level, an incorrect one shows an "Incorrect!
Try again." message. The current levels cover: variables, conditionals (`if`), loops (`for`),
functions (`def`), strings, and lists.

## Status

An early, small-scale learning project (first and only feature commit is tagged `version0.5`).
It has not been developed further since; the only later commit removed accidentally tracked
`__pycache__` files and added a `.gitignore`.

## Requirements

- Python 3
- [pygame](https://www.pygame.org/) (the only external dependency imported by the source)

```
pip install pygame
```

## Running

Run from the repository root, since the game loads `levels.json` using a path relative to the
current working directory:

```
python main.py
```
