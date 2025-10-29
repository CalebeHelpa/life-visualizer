"""Matplotlib based visualizer for Conway's Game of Life."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .simulation import GameOfLife


@dataclass
class GameOfLifeVisualizer:
    """Interactive matplotlib visualizer for the Game of Life."""

    game: GameOfLife
    interval: int = 100
    title: str = "Conway's Game of Life"
    cmap: str = "viridis"
    start_paused: bool = True
    paused: bool = field(default=False, init=False)
    last_fps_update: float = field(default_factory=time.time, init=False)
    frames_since_update: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        plt.style.use("dark_background")
        self.figure, self.ax = plt.subplots(figsize=(10, 6), dpi=100)
        self.figure.canvas.mpl_connect("key_press_event", self._on_key_press)
        self.figure.canvas.mpl_connect("button_press_event", self._on_click)
        self.paused = self.start_paused
        self.image = self.ax.imshow(
            self.game.state,
            interpolation="nearest",
            cmap=self.cmap,
            vmin=0,
            vmax=1,
        )
        self.ax.set_title(self.title, fontsize=16, pad=20)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.status = self.ax.text(
            0.02,
            0.98,
            self._status_text(),
            transform=self.ax.transAxes,
            ha="left",
            va="top",
            color="white",
            fontsize=10,
            bbox=dict(facecolor="black", alpha=0.5, boxstyle="round,pad=0.3"),
        )
        self.animation = FuncAnimation(
            self.figure,
            self._update,
            interval=self.interval,
            blit=True,
        )

    def _status_text(self) -> str:
        mode = "Paused" if self.paused else "Running"
        alive_pct = 100 * self.game.alive_ratio
        return (
            f"{mode}\n"
            f"{self.game.rows}×{self.game.cols} | alive {alive_pct:.1f}%"
        )

    def _update(self, _frame: int):
        if not self.paused:
            self.game.step()
        self.image.set_data(self.game.state)
        self.frames_since_update += 1
        self._update_fps()
        self.status.set_text(self._status_text())
        return (self.image, self.status)

    def _update_fps(self) -> None:
        now = time.time()
        elapsed = now - self.last_fps_update
        if elapsed >= 1.0:
            fps = self.frames_since_update / elapsed
            manager = getattr(self.figure.canvas, "manager", None)
            if manager is not None and hasattr(manager, "set_window_title"):
                manager.set_window_title(f"{self.title} – {fps:.1f} FPS")
            self.last_fps_update = now
            self.frames_since_update = 0

    def _on_key_press(self, event) -> None:
        if event.key == "space":
            self.paused = not self.paused
        elif event.key == "r":
            self.game.randomize()
        elif event.key == "c":
            self.game.clear()
        elif event.key == "up":
            self._adjust_speed(-10)
        elif event.key == "down":
            self._adjust_speed(10)
        elif event.key == "+":
            self._adjust_density(0.05)
        elif event.key == "-":
            self._adjust_density(-0.05)

    def _on_click(self, event) -> None:
        if event.inaxes != self.ax:
            return
        if event.xdata is None or event.ydata is None:
            return
        col = int(round(event.xdata))
        row = int(round(event.ydata))
        col = max(0, min(self.game.cols - 1, col))
        row = max(0, min(self.game.rows - 1, row))
        self.game.toggle(row, col)
        self.image.set_data(self.game.state)
        self.figure.canvas.draw_idle()

    def _adjust_speed(self, delta: int) -> None:
        new_interval = max(10, self.interval + delta)
        if new_interval != self.interval:
            self.interval = new_interval
            self.animation.event_source.interval = self.interval

    def _adjust_density(self, delta: float) -> None:
        new_density = float(min(max(self.game.density + delta, 0.0), 1.0))
        if new_density != self.game.density:
            self.game.randomize(new_density)

    def show(self) -> None:
        """Start the matplotlib event loop and display the animation."""

        plt.show()
