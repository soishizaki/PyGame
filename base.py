"""
Módulo base do jogo Maze Kitty Treasure Hunt.

Aqui ficam:
- as imagens do labirinto e do jogador,
- o desenho das fases (fácil, médio, difícil),
- as funções para desenhar o labirinto/jogador na tela
- e a lógica para trocar de fase e validar movimentos.
"""

import pygame
from pathlib import Path

# --- Configurações do labirinto (tamanho de cada "quadradinho") ---
TAMANHO_CELULA = 600 // 25

# pasta onde estão as imagens
img = Path("img")

# --- Tiles do cenário (grama, madeira e tesouros) ---

# bloco de grama (parede)
tile_grass = pygame.transform.scale(
    pygame.image.load(img / "tile-grass.png"),
    (int(TAMANHO_CELULA), int(TAMANHO_CELULA))
)

# bloco de madeira (caminho)
tile_wood = pygame.transform.scale(
    pygame.image.load(img / "tile-wood.png"),
    (int(TAMANHO_CELULA), int(TAMANHO_CELULA))
)

# moedas / tesouros (prata, ouro, diamante) 
prata = pygame.image.load(img / "prata.png")
prata = pygame.transform.smoothscale(
    prata,
    (int(TAMANHO_CELULA), int(TAMANHO_CELULA))
)

ouro = pygame.image.load(img / "ouro.png")
ouro = pygame.transform.smoothscale(
    ouro,
    (int(TAMANHO_CELULA), int(TAMANHO_CELULA))
)

diamante = pygame.image.load(img / "diamante.png")
diamante = pygame.transform.smoothscale(
    diamante,
    (int(TAMANHO_CELULA), int(TAMANHO_CELULA))
)

# --- Configuração da imagem do jogador (gatinho) ---
TAMANHO_JOGADOR = int(TAMANHO_CELULA * 0.9)

jogador_img = pygame.image.load(img / "gato.png")
jogador_img = pygame.transform.smoothscale(
    jogador_img,
    (TAMANHO_JOGADOR, TAMANHO_JOGADOR)
)

# ---Definição dos labirintos (matrizes)---
# 1 = parede, 0 = caminho, 2/3/4 = tesouros/saídas especiais

LABIRINTO_MEDIO = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,0,1,1,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1],
    [1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,3],
    [1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

LABIRINTO_FACIL = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,1,1],
    [1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,1,1,1],
    [1,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,1],
    [1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1],
    [1,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1,0,1,1],
    [1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,1],
    [1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1,1,0,1,1,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,1],
    [1,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1,1],
    [1,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,1],
    [1,1,0,0,0,1,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,0,0,2],
    [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

LABIRINTO_DIFICIL = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,1],
    [1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1],
    [1,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,1],
    [1,1,0,1,0,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,0,1,0,1,1],
    [1,1,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,0,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1],
    [1,1,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1],
    [1,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,0,0,1,1],
    [1,1,1,1,1,1,0,1,1,1,0,1,1,1,0,0,0,1,0,1,1,1,0,1,1],
    [1,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,0,0,1,1],
    [1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,0,1,0,1,1,1,1],
    [1,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,1],
    [1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,1,1],
    [1,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,4],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# --- Lista de fases e estado atual ---
FASES = [LABIRINTO_FACIL, LABIRINTO_MEDIO, LABIRINTO_DIFICIL]
fase_atual = 0

# labirinto que está sendo usado no momento
LABIRINTO = FASES[fase_atual]


def calcular_offset(tela):
    """
    Calcula o deslocamento (offset) para centralizar o labirinto na tela.
    Isso permite que o labirinto seja menor que a janela, mas fique no meio.
    """
    linhas = len(LABIRINTO)
    colunas = len(LABIRINTO[0])

    largura_total = colunas * TAMANHO_CELULA
    altura_total = linhas * TAMANHO_CELULA

    offset_x = (tela.get_width()  - largura_total) / 2
    offset_y = (tela.get_height() - altura_total) / 2

    return offset_x, offset_y


def encontrar_inicio():
    """
    Procura a primeira célula igual a 0 no labirinto atual
    e usa como ponto de partida do jogador.
    """
    for i, row in enumerate(LABIRINTO):
        for j, v in enumerate(row):
            if v == 0:
                return [i, j]
    # Se não encontrar nenhum 0, usa o centro do labirinto como fallback
    return [len(LABIRINTO) // 2, len(LABIRINTO[0]) // 2]


def carregar_fase(indice):
    """
    Troca a fase atual pelo índice informado.
    Atualiza o LABIRINTO global para apontar para a nova fase.
    """
    global LABIRINTO, fase_atual
    fase_atual = indice
    LABIRINTO = FASES[fase_atual]


# garante que LABIRINTO esteja sincronizado com fase_atual
LABIRINTO = FASES[fase_atual]


def desenhar_labirinto(tela):
    """
    Desenha o labirinto completo na tela, célula por célula,
    com o tile correto para cada tipo de valor da matriz.
    """
    offset_x, offset_y = calcular_offset(tela)

    for linha, row in enumerate(LABIRINTO):
        for coluna, cell in enumerate(row):
            x = int(offset_x + coluna * TAMANHO_CELULA)
            y = int(offset_y + linha  * TAMANHO_CELULA)

            if cell == 1:
                # parede de grama
                tela.blit(tile_grass, (x, y))
            elif cell == 0:
                # caminho simples
                tela.blit(tile_wood, (x, y))
            elif cell == 2:
                # caminho com prata
                tela.blit(tile_wood, (x, y))
                tela.blit(prata, (x, y))
            elif cell == 3:
                # caminho com ouro
                tela.blit(tile_wood, (x, y))
                tela.blit(ouro, (x, y))
            else:
                # qualquer outro valor vira diamante (4, etc.)
                tela.blit(tile_wood, (x, y))
                tela.blit(diamante, (x, y))


# --- Configurações do jogador ---
POS_INICIAL = encontrar_inicio()


def desenhar_jogador(tela, posicao):
    """
    Desenha o gatinho na célula indicada por (linha, coluna),
    centralizando a imagem dentro do quadradinho.
    """
    linha, coluna = posicao
    offset_x, offset_y = calcular_offset(tela)

    # margem para o gatinho não ficar colado na borda da célula
    margem = (TAMANHO_CELULA - TAMANHO_JOGADOR) // 2

    x = int(offset_x + coluna * TAMANHO_CELULA + margem)
    y = int(offset_y + linha  * TAMANHO_CELULA + margem)

    tela.blit(jogador_img, (x, y))


def posicao_valida(linha, coluna):
    """
    Verifica se a posição está dentro do labirinto
    e não é parede (1). Retorna True/False.
    """
    if linha < 0 or linha >= len(LABIRINTO):
        return False
    if coluna < 0 or coluna >= len(LABIRINTO[0]):
        return False
    return LABIRINTO[linha][coluna] != 1
