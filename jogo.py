"""
Arquivo principal do jogo Maze Kitty Treasure Hunt.

Aqui controlamos:
- a janela do jogo, áudio e fontes,
- o menu inicial e as telas de instruções (2 páginas),
- as telas de próxima fase e de vitória (com animação de estrelinhas),
- o loop principal do jogo (movimento, timer por fase e troca de fases).
"""

import pygame
import sys
import base
from base import *
import random

pygame.init()
pygame.mixer.init() 

# --- Música de fundo (loop infinito) ---
pygame.mixer.music.load("sons/fundo.mp3")
pygame.mixer.music.set_volume(0.4)
pygame.mixer.music.play(-1)

# --- Som de botão (clicar em play, info, etc) ---
SOM_BOTAO = pygame.mixer.Sound("sons/botao.mp3")
SOM_BOTAO.set_volume(0.8)

# --- Configurações da tela do jogo ---
LARGURA_TELA = 600
ALTURA_TELA = 600
TITULO_JOGO = "Maze Kitty Treasure Hunt"
COR_FUNDO = (30, 30, 30)
COR_TEXTO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO_JOGO)
clock = pygame.time.Clock()

# --- Timer por fase (quantos segundos o jogador tem) ---
TEMPO_FASE = 31  
FONT_TEMPO = pygame.font.SysFont("Arial", 15, bold=True)

# --- Imagens principais do jogo (menu, próxima fase, fim) ---
IMG_INICIO = pygame.image.load("img/inicio.png").convert()
IMG_INICIO = pygame.transform.smoothscale(IMG_INICIO, (LARGURA_TELA, ALTURA_TELA))

IMG_PROXIMA = pygame.image.load("img/proxima_fase.png").convert()
IMG_PROXIMA = pygame.transform.smoothscale(IMG_PROXIMA, (LARGURA_TELA, ALTURA_TELA))

IMG_FINAL = pygame.image.load("img/fim.png").convert()
IMG_FINAL = pygame.transform.smoothscale(IMG_FINAL, (LARGURA_TELA, ALTURA_TELA))

# ---Telas de instruções---
# infos1: explicando movimento / controles
IMG_INFO1 = pygame.image.load("img/infos1.png").convert()
IMG_INFO1 = pygame.transform.smoothscale(IMG_INFO1, (LARGURA_TELA, ALTURA_TELA))

# infos2: explicando o tempo por fase e o "volta pra fase 1"
IMG_INFO2 = pygame.image.load("img/infos2.png").convert()
IMG_INFO2 = pygame.transform.smoothscale(IMG_INFO2, (LARGURA_TELA, ALTURA_TELA))


# --- Telas de informações (Instructions, com navegação Next/Back) ---
def tela_infos():
    """
    Exibe as telas de instruções.
    Página 1: mostra os controles (setinhas).
    Página 2: explica o tempo por fase.
    O botão no canto inferior direito muda de Next para Back.
    """
    # botão no canto inferior direito (mesmo lugar nas duas imagens)
    botao_rect = pygame.Rect(LARGURA_TELA - 170, ALTURA_TELA - 80, 142, 60)

    pagina = 1  

    while True:
        # desenha a página atual
        if pagina == 1:
            tela.blit(IMG_INFO1, (0, 0))
        else:
            tela.blit(IMG_INFO2, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # ESC fecha o jogo diretamente
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    SOM_BOTAO.play()
                    if pagina == 1:
                        pagina = 2
                    else:
                        return  # volta pro menu

                if pagina == 2 and evento.key == pygame.K_BACKSPACE:
                    SOM_BOTAO.play()
                    return

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # clique no botão Next/Back
                if botao_rect.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    if pagina == 1:
                        pagina = 2     
                    else:
                        return      

        pygame.display.flip()
        clock.tick(60)


# --- Tela de menu inicial (Play + Info) ---
def menu_inicial():
    """
    Exibe o menu inicial com:
    - botão Play para começar o jogo,
    - botão Info para abrir as instruções.
    """
    botao_play = pygame.Rect(
        LARGURA_TELA // 2 - 130,
        ALTURA_TELA - 120,
        260,
        60
    )

    botao_info = pygame.Rect(
        LARGURA_TELA - 115,
        480,
        70,
        70
    )

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(IMG_INICIO, (0, 0))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                # ESC fecha o jogo
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    SOM_BOTAO.play()
                    return
                if evento.key == pygame.K_i:
                    SOM_BOTAO.play()
                    tela_infos()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # clique no PLAY
                if botao_play.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return
                # clique no INFO
                if botao_info.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    tela_infos()

        pygame.display.flip()
        clock.tick(60)


# --- estrelas: cores e criação de estrelinhas ---

# Cores possíveis para as estrelinhas
CORES_ESTRELAS = [
    (255, 255, 0),   # amarelo
    (255, 192, 203), # rosa
    (135, 206, 250), # azul claro
    (144, 238, 144), # verde claro
    (255, 165, 0),   # laranja
    (255, 255, 255)  # branco
]

def criar_estrela(multicolor=False):
    """
    Cria uma estrelinha que começa caindo de algum ponto acima da tela.
    Se multicolor=True, escolhe uma cor aleatória da lista.
    Caso contrário, usa amarelo.
    """
    cor = random.choice(CORES_ESTRELAS) if multicolor else (255, 255, 0)
    return {
        "x": random.randint(0, LARGURA_TELA),
        "y": random.randint(-ALTURA_TELA, 0),
        "vel": random.uniform(1.5, 4.0),
        "raio": random.randint(2, 4),
        "cor": cor
    }


# --- Tela de próxima fase ---
def tela_proxima_fase():
    """
    Mostra a tela de 'Next Level' com estrelinhas amarelas caindo.
    O jogador pode apertar Enter/Espaço ou clicar no botão para avançar.
    """
    botao_next = pygame.Rect(
        LARGURA_TELA // 2 - 200,
        ALTURA_TELA - 180,
        400,
        100
    )

    # cria várias estrelinhas iniciais (amarelas)
    estrelas = [criar_estrela() for _ in range(300)]
    rodando = True

    while rodando:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    SOM_BOTAO.play()
                    return

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_next.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return

        # atualiza posição das estrelinhas
        for e in estrelas:
            e["y"] += e["vel"]
            # quando passa da parte de baixo, recria lá em cima
            if e["y"] > ALTURA_TELA + 10:
                novo = criar_estrela()
                e["x"] = novo["x"]
                e["y"] = novo["y"]
                e["vel"] = novo["vel"]
                e["raio"] = novo["raio"]

        # desenha o fundo da tela de próxima fase
        tela.blit(IMG_PROXIMA, (0, 0))

        # desenha as estrelinhas por cima
        for e in estrelas:
            pygame.draw.circle(
                tela,
                (255, 255, 0),  # amarelo estrela
                (int(e["x"]), int(e["y"])),
                e["raio"]
            )

        pygame.display.flip()


# --- Tela de final/restart (vitória, com estrelinhas coloridas) ---
def tela_final():
    """
    Mostra a tela de vitória do jogo:
    - fundo de 'fim',
    - chuva de estrelinhas coloridas,
    - botão para reiniciar o jogo.
    """
    botao_play = pygame.Rect(
        LARGURA_TELA // 2 - 205,
        ALTURA_TELA - 180,
        410,
        95
    )

    # estrelinhas na tela de vitória
    estrelas = [criar_estrela(multicolor=True) for _ in range(500)]

    while True:
        clock.tick(60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                    SOM_BOTAO.play()
                    return "reiniciar"

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_play.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return "reiniciar"

        # atualiza estrelas
        for e in estrelas:
            e["y"] += e["vel"]
            if e["y"] > ALTURA_TELA + 10:
                novo = criar_estrela(multicolor=True)
                e["x"], e["y"], e["vel"], e["raio"], e["cor"] = \
                    novo["x"], novo["y"], novo["vel"], novo["raio"], novo["cor"]

        # desenha o fundo de vitória
        tela.blit(IMG_FINAL, (0, 0))

        # desenha estrelas por cima
        for e in estrelas:
            pygame.draw.circle(
                tela,
                e["cor"],
                (int(e["x"]), int(e["y"])),
                e["raio"]
            )

        pygame.display.flip()


# --- Loop principal do jogo (fases, movimento, timer) ---
def main():
    """
    Loop principal do jogo:
    - mostra o menu,
    - controla o movimento do jogador dentro do labirinto,
    - gerencia o timer por fase,
    - troca de fase ao vencer e trata a tela final.
    """
    menu_inicial()  # mostra o menu antes de começar

    pos_jogador = base.encontrar_inicio()
    vitoria = False
    rodando = True

    # início do relógio da fase (em milissegundos)
    tempo_inicial = pygame.time.get_ticks()

    while rodando:
        clock.tick(30)

        # --- TRATAMENTO DE EVENTOS (teclado / janela) ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN:
                # ESC fecha o jogo a partir da fase
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                # movimento só é permitido enquanto não venceu
                if not vitoria:
                    nova_linha, nova_coluna = pos_jogador

                    if evento.key == pygame.K_UP:
                        nova_linha -= 1
                    elif evento.key == pygame.K_DOWN:
                        nova_linha += 1
                    elif evento.key == pygame.K_LEFT:
                        nova_coluna -= 1
                    elif evento.key == pygame.K_RIGHT:
                        nova_coluna += 1

                    # só anda se a posição for válida
                    if posicao_valida(nova_linha, nova_coluna):
                        pos_jogador = [nova_linha, nova_coluna]
                        # se pisar em uma célula de saída/tesouro (2, 3, 4), marca vitória
                        if base.LABIRINTO[nova_linha][nova_coluna] in (2, 3, 4):
                            vitoria = True

        # ---tempo ---
        segundos_decorridos = (pygame.time.get_ticks() - tempo_inicial) / 1000
        tempo_restante = max(0, int(TEMPO_FASE - segundos_decorridos))

        # se o tempo acabar e ainda não venceu: volta para o primeiro mapa
        if tempo_restante <= 0 and not vitoria:
            base.fase_atual = 0
            carregar_fase(0)
            pos_jogador = base.encontrar_inicio()
            vitoria = False
            tempo_inicial = pygame.time.get_ticks()  
            continue

        # ---labirinto + jogador + timer---
        tela.fill(COR_FUNDO)
        desenhar_labirinto(tela)
        desenhar_jogador(tela, pos_jogador)

        # desenha o relógio no canto superior esquerdo
        texto_tempo = FONT_TEMPO.render(
            f"Timer: {tempo_restante:02d} seconds",
            True,
            COR_TEXTO
        )
        tela.blit(texto_tempo, (15, 5))

        pygame.display.flip()

        # tela vitoria
        if vitoria:
            if base.fase_atual < len(base.FASES) - 1:
                # mostra a tela proximo nivel antes de seguir
                tela_proxima_fase()
                carregar_fase(base.fase_atual + 1)
                pos_jogador = base.encontrar_inicio()
                vitoria = False
                tempo_inicial = pygame.time.get_ticks()
            else:
                # chegou na última fase e venceu, vai pra tela final
                escolha = tela_final()
                if escolha == "reiniciar":
                    carregar_fase(0)
                    base.fase_atual = 0
                    pos_jogador = base.encontrar_inicio()
                    vitoria = False
                    tempo_inicial = pygame.time.get_ticks()
                else:
                    rodando = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
