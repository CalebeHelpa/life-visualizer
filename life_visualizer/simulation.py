"""Core simulation logic for Conway's Game of Life."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class GameOfLife:
    """Manage the state and evolution of Conway's Game of Life."""

    rows: int
    cols: int
    density: float = 0.2
    wrap: bool = True
    seed: Optional[int] = None
    initial_state: Optional[np.ndarray] = None

    def __post_init__(self) -> None:
        self.random = np.random.default_rng(self.seed)
        if self.initial_state is not None:
            state = np.array(self.initial_state, dtype=np.uint8, copy=True)
            if state.shape != (self.rows, self.cols):
                raise ValueError(
                    "initial_state must match the configured board dimensions"
                )
            self.state = state
        else:
            self.state = self._generate_random_state(self.density)

    def _generate_random_state(self, density: float) -> np.ndarray:
        density = float(np.clip(density, 0.0, 1.0))
        return (self.random.random((self.rows, self.cols)) < density).astype(np.uint8)

    def step(self) -> np.ndarray:
        """Advance the simulation by one tick and return the new state."""

        neighbors = self._count_neighbors()
        survives = (self.state == 1) & ((neighbors == 2) | (neighbors == 3))
        born = (self.state == 0) & (neighbors == 3)
        self.state[...] = 0
        self.state[survives | born] = 1
        return self.state

    def _count_neighbors(self) -> np.ndarray:
        """Count neighbours for each cell using numpy roll operations."""

        offsets = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1),
        ]

        neighbors = np.zeros_like(self.state, dtype=np.uint8)

        if self.wrap:
            for dy, dx in offsets:
                neighbors += np.roll(np.roll(self.state, dy, axis=0), dx, axis=1)
        else:
            padded = np.pad(self.state, 1, mode="constant")
            for dy, dx in offsets:
                neighbors += padded[1 + dy : 1 + dy + self.rows, 1 + dx : 1 + dx + self.cols]
        return neighbors

    def randomize(self, density: Optional[float] = None) -> None:
        """Re-seed the board using the provided density."""

        if density is not None:
            self.density = float(np.clip(density, 0.0, 1.0))
        self.state = self._generate_random_state(self.density)

    @property
    def alive_ratio(self) -> float:
        """Return the fraction of alive cells in the current state."""

        if self.state.size == 0:
            return 0.0
        return float(self.state.mean())

    def clear(self) -> None:
        """Clear the board, leaving all cells dead."""

        self.state[...] = 0

    def toggle(self, row: int, col: int) -> None:
        """Toggle a single cell from alive to dead or vice-versa."""

        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.state[row, col] = 1 - self.state[row, col]

    def resize(self, rows: int, cols: int) -> None:
        """Resize the board, preserving as much of the current state as possible."""

        rows = int(max(1, rows))
        cols = int(max(1, cols))
        new_state = np.zeros((rows, cols), dtype=np.uint8)
        min_rows = min(rows, self.state.shape[0])
        min_cols = min(cols, self.state.shape[1])
        new_state[:min_rows, :min_cols] = self.state[:min_rows, :min_cols]
        self.rows, self.cols = rows, cols
        self.state = new_state
