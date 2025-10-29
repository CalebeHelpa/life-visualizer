"""Command line entry point for running the visualizer."""
from __future__ import annotations

import argparse

from .simulation import GameOfLife
from .visualizer import GameOfLifeVisualizer


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Visualizador interativo do Jogo da Vida de John Conway, "
            "ideal para apresentações. Use as setas para ajustar a velocidade, "
            "espaço para pausar e o rato para ligar/desligar células."
        )
    )
    parser.add_argument("--rows", type=int, default=80, help="Número de linhas do tabuleiro")
    parser.add_argument("--cols", type=int, default=120, help="Número de colunas do tabuleiro")
    parser.add_argument(
        "--density",
        type=float,
        default=0.25,
        help="Densidade inicial de células vivas (0 a 1)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=80,
        help="Intervalo entre frames em milissegundos",
    )
    parser.add_argument(
        "--wrap",
        action="store_true",
        help="Ativa contorno toroidal (bordas conectadas)",
    )
    parser.add_argument(
        "--no-wrap",
        dest="wrap",
        action="store_false",
        help="Desativa contorno toroidal (bordas rígidas)",
    )
    parser.set_defaults(wrap=True)
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Semente para o gerador aleatório (permite reproduzir o padrão)",
    )
    parser.add_argument(
        "--cmap",
        default="viridis",
        help="Mapa de cores do matplotlib a utilizar",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    game = GameOfLife(
        rows=max(5, args.rows),
        cols=max(5, args.cols),
        density=args.density,
        wrap=args.wrap,
        seed=args.seed,
    )
    visualizer = GameOfLifeVisualizer(
        game,
        interval=max(10, args.interval),
        cmap=args.cmap,
    )
    visualizer.show()


if __name__ == "__main__":
    main()
