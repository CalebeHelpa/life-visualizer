# life-visualizer

Visualizador interativo do **Jogo da Vida** de John Conway escrito em Python.

## Pré-requisitos

- Python 3.9 ou superior
- Dependências listadas em `requirements.txt`

Instale-as com:

```bash
python -m venv .venv
source .venv/bin/activate  # No Windows use .venv\Scripts\activate
pip install -r requirements.txt
```

## Como executar

Execute o visualizador a partir da raiz do repositório:

```bash
python -m life_visualizer --rows 80 --cols 120 --density 0.25 --interval 80
```

### Controles

- **Espaço**: pausa/retoma a simulação
- **Seta para cima/baixo**: acelera ou desacelera a animação
- **R**: gera um novo tabuleiro aleatório com a densidade atual
- **C**: limpa o tabuleiro
- **+/-**: aumenta ou diminui a densidade e reinicia o tabuleiro
- **Clique esquerdo**: alterna o estado da célula clicada

### Opções úteis

- `--wrap` / `--no-wrap`: alterna entre bordas conectadas (toro) ou rígidas
- `--seed`: fixa a semente aleatória para padrões reprodutíveis
- `--cmap`: escolhe o mapa de cores do Matplotlib

A janela mostra continuamente o estado atual da simulação, perfeito para deixar em execução durante apresentações.
