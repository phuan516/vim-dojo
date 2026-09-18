"""Terminal rendering primitives for vim-dojo."""
import os
import shutil
import sys

_NO_COLOR = os.environ.get("NO_COLOR") or not sys.stdout.isatty()


def _c(code):
    return "" if _NO_COLOR else f"\033[{code}m"


R = _c(0)
B = _c(1)
D = _c(2)
IT = _c(3)
RED = _c(31)
GRN = _c(32)
YEL = _c(33)
BLU = _c(34)
MAG = _c(35)
CYA = _c(36)
WHT = _c(37)
GREY = _c("38;5;244")

BELT_COLOR = {
    "white": WHT,
    "yellow": YEL,
    "orange": _c("38;5;208"),
    "green": GRN,
    "blue": BLU,
    "purple": MAG,
    "brown": _c("38;5;137"),
    "black": GREY,
}


def width(default=80):
    return min(shutil.get_terminal_size((default, 24)).columns, 92)


def rule(char="─"):
    print(f"{D}{char * width()}{R}")


def title(text, colour=CYA):
    print(f"\n{B}{colour}  {text}{R}")


def dim(text):
    print(f"{D}{text}{R}")


def indent(text, pad="  "):
    for line in text.rstrip("\n").split("\n"):
        print(pad + line)


def bar(done, total, size=22, colour=GRN):
    if total <= 0:
        total = 1
    filled = int(round(size * min(done / total, 1.0)))
    return f"{colour}{'█' * filled}{R}{D}{'░' * (size - filled)}{R}"


def belt_tag(belt):
    colour = BELT_COLOR.get(belt, WHT)
    return f"{colour}●{R} {belt}"


def kv(key, value, keyw=14):
    print(f"  {D}{key:<{keyw}}{R}{value}")


def banner():
    print(f"\n{B}{MAG}  ⚔  vim-dojo{R}  {D}— a year of deliberate practice{R}\n")
