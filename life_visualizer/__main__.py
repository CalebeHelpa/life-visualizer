"""Command line entry point for running the visualizer."""
from __future__ import annotations

import argparse

from .banner import DEFAULT_MESSAGE, create_banner_board
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
    parser.add_argument(
        "--rows",
        type=int,
        default=180,
        help="Número mínimo de linhas do tabuleiro (ajustado automaticamente se necessário)",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=640,
        help="Número mínimo de colunas do tabuleiro (ajustado automaticamente se necessário)",
    )
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
    banner_state = create_banner_board(
        max(5, args.rows),
        max(5, args.cols),
        text=DEFAULT_MESSAGE,
        scale=3,
        spacing=1,
        margin=12,
    )

    game = GameOfLife(
        rows=banner_state.shape[0],
        cols=banner_state.shape[1],
        density=args.density,
        wrap=args.wrap,
        seed=args.seed,
        initial_state=banner_state,
    )
    visualizer = GameOfLifeVisualizer(
        game,
        interval=max(10, args.interval),
        cmap=args.cmap,
        start_paused=True,
    )
    visualizer.show()


if __name__ == "__main__":
    main()
