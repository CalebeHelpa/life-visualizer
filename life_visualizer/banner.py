"""Utilities to render the presentation banner for the Game of Life visualizer."""
from __future__ import annotations

from typing import Dict, Iterable, List

import numpy as np


DEFAULT_MESSAGE = "// while(true){filosofar(?);}"  # noqa: S105 - presentation message

_FONT_5x7: Dict[str, List[str]] = {
    " ": [
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
        "     ",
    ],
    "/": [
        "    #",
        "   # ",
        "   # ",
        "  #  ",
        " #   ",
        "#    ",
        "#    ",
    ],
    "w": [
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "# # #",
        "# # #",
        " # # ",
    ],
    "h": [
        "#    ",
        "#    ",
        "#    ",
        "#####",
        "#   #",
        "#   #",
        "#   #",
    ],
    "i": [
        " ### ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        " ### ",
    ],
    "l": [
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#    ",
        "#####",
    ],
    "e": [
        " ####",
        "#    ",
        "#    ",
        "#### ",
        "#    ",
        "#    ",
        " ####",
    ],
    "(": [
        "   # ",
        "  #  ",
        " #   ",
        " #   ",
        " #   ",
        "  #  ",
        "   # ",
    ],
    "t": [
        "#####",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
        "  #  ",
    ],
    "r": [
        "#### ",
        "#   #",
        "#   #",
        "#### ",
        "# #  ",
        "#  # ",
        "#   #",
    ],
    "u": [
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " ### ",
    ],
    ")": [
        "#    ",
        " #   ",
        "  #  ",
        "  #  ",
        "  #  ",
        " #   ",
        "#    ",
    ],
    "{": [
        "   ##",
        "  #  ",
        "  #  ",
        "##   ",
        "  #  ",
        "  #  ",
        "   ##",
    ],
    "}": [
        "##   ",
        "  #  ",
        "  #  ",
        "   ##",
        "  #  ",
        "  #  ",
        "##   ",
    ],
    "f": [
        "#####",
        "#    ",
        "#    ",
        "#### ",
        "#    ",
        "#    ",
        "#    ",
    ],
    "o": [
        " ### ",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        "#   #",
        " ### ",
    ],
    "s": [
        " ####",
        "#    ",
        "#    ",
        " ### ",
        "    #",
        "    #",
        "#### ",
    ],
    "a": [
        " ### ",
        "#   #",
        "#   #",
        "#####",
        "#   #",
        "#   #",
        "#   #",
    ],
    "?": [
        " ### ",
        "#   #",
        "    #",
        "   # ",
        "  #  ",
        "     ",
        "  #  ",
    ],
    ";": [
        "     ",
        "  #  ",
        "     ",
        "     ",
        "  #  ",
        "  #  ",
        " #   ",
    ],
}


def _render_character(char: str) -> np.ndarray:
    try:
        glyph = _FONT_5x7[char]
    except KeyError as exc:  # pragma: no cover - defensive branch
        raise ValueError(f"Unsupported character: {char!r}") from exc
    return np.array([[1 if pixel == "#" else 0 for pixel in row] for row in glyph], dtype=np.uint8)


def _render_text_rows(text: str, spacing: int) -> Iterable[np.ndarray]:
    for index, char in enumerate(text):
        glyph = _render_character(char)
        if index < len(text) - 1 and spacing > 0:
            padding = np.zeros((glyph.shape[0], spacing), dtype=np.uint8)
            yield glyph
            yield padding
        else:
            yield glyph


def render_text_pattern(text: str, spacing: int = 1) -> np.ndarray:
    """Render *text* into a binary numpy array using the built-in 5x7 font."""

    glyphs = list(_render_text_rows(text, spacing))
    if not glyphs:
        return np.zeros((0, 0), dtype=np.uint8)
    return np.concatenate(glyphs, axis=1)


def upscale_pattern(pattern: np.ndarray, scale: int) -> np.ndarray:
    """Upscale a pattern by the given integer *scale*."""

    scale = int(max(1, scale))
    if scale == 1 or pattern.size == 0:
        return pattern
    factor = np.ones((scale, scale), dtype=np.uint8)
    return np.kron(pattern, factor)


def create_banner_board(
    rows: int,
    cols: int,
    *,
    text: str = DEFAULT_MESSAGE,
    scale: int = 3,
    spacing: int = 1,
    margin: int = 8,
) -> np.ndarray:
    """Create a board with *text* centered and padded within the given dimensions."""

    base_pattern = render_text_pattern(text, spacing=spacing)
    pattern = upscale_pattern(base_pattern, scale)

    min_rows = pattern.shape[0] + 2 * margin
    min_cols = pattern.shape[1] + 2 * margin
    total_rows = max(rows, min_rows)
    total_cols = max(cols, min_cols)

    board = np.zeros((total_rows, total_cols), dtype=np.uint8)
    if pattern.size == 0:
        return board

    top = (total_rows - pattern.shape[0]) // 2
    left = (total_cols - pattern.shape[1]) // 2
    board[top : top + pattern.shape[0], left : left + pattern.shape[1]] = pattern
    return board
