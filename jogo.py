import pygame
import sys
import base
from base import *

pygame.init()
pygame.mixer.init()  # inicializa o áudio

# --- Música de fundo ---
pygame.mixer.music.load("sons/fundo.mp3")  # carrega a música de fundo
pygame.mixer.music.set_volume(0.4)         # volume da trilha (0.0 a 1.0)
pygame.mixer.music.play(-1)                # -1 = loop infinito

# --- Som de botão ---
SOM_BOTAO = pygame.mixer.Sound("sons/botao.mp3")
SOM_BOTAO.set_volume(0.8)  # volume do som de clique

# --- Config da tela ---
LARGURA_TELA = 800
ALTURA_TELA = 800
TITULO_JOGO = "Maze Kitty Treasure Hunt"
COR_FUNDO = (30, 30, 30)
COR_TEXTO = (255, 255, 255)

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption(TITULO_JOGO)
clock = pygame.time.Clock()

# === imagens ===
IMG_INICIO = pygame.image.load("img/inicio.png").convert()
IMG_INICIO = pygame.transform.smoothscale(IMG_INICIO, (LARGURA_TELA, ALTURA_TELA))

IMG_PROXIMA = pygame.image.load("img/proxima_fase.png").convert()
IMG_PROXIMA = pygame.transform.smoothscale(IMG_PROXIMA, (LARGURA_TELA, ALTURA_TELA))

IMG_FINAL = pygame.image.load("img/fim.png").convert()
IMG_FINAL = pygame.transform.smoothscale(IMG_FINAL, (LARGURA_TELA, ALTURA_TELA))


# --- Tela de menu inicial ---
def menu_inicial():
    botao_play = pygame.Rect(LARGURA_TELA // 2 - 180, 620, 360, 90)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(IMG_INICIO, (0, 0))

        # brilho opcional ao passar o mouse
        if botao_play.collidepoint(mouse_pos):
            s = pygame.Surface((botao_play.width, botao_play.height), pygame.SRCALPHA)
            s.fill((255, 255, 255, 25))
            tela.blit(s, botao_play.topleft)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_play.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                SOM_BOTAO.play()
                return

        pygame.display.flip()
        clock.tick(60)


# --- Tela de próxima fase ---
def tela_proxima_fase():
    botao_next = pygame.Rect(LARGURA_TELA // 2 - 200, 620, 400, 100)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(IMG_PROXIMA, (0, 0))

        # hover
        if botao_next.collidepoint(mouse_pos):
            s = pygame.Surface((botao_next.width, botao_next.height), pygame.SRCALPHA)
            s.fill((255, 255, 255, 20))
            tela.blit(s, botao_next.topleft)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_next.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                SOM_BOTAO.play()
                return

        pygame.display.flip()
        clock.tick(60)


# --- Tela de final/restart ---
def tela_final():
    botao_play = pygame.Rect(LARGURA_TELA // 2 - 205, 617, 410, 95)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(IMG_FINAL, (0, 0))

        # botão opaco com leve brilho no hover
        s = pygame.Surface((botao_play.width, botao_play.height), pygame.SRCALPHA)
        if botao_play.collidepoint(mouse_pos):
            s.fill((255, 255, 255, 40))  # brilho no hover
        else:
            s.fill((255, 255, 255, 15))  # leve opacidade padrão
        tela.blit(s, botao_play.topleft)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if botao_play.collidepoint(evento.pos):
                    SOM_BOTAO.play()
                    return "reiniciar"

            if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                SOM_BOTAO.play()
                return "reiniciar"

        pygame.display.flip()
        clock.tick(60)


# --- Loop principal do jogo ---
def main():
    menu_inicial()  # escolhe a fase inicial (dificuldade)

    pos_jogador = base.encontrar_inicio()
    vitoria = False
    rodando = True

    while rodando:
        clock.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False

            if evento.type == pygame.KEYDOWN and not vitoria:
                nova_linha, nova_coluna = pos_jogador

                if evento.key == pygame.K_UP:
                    nova_linha -= 1
                elif evento.key == pygame.K_DOWN:
                    nova_linha += 1
                elif evento.key == pygame.K_LEFT:
                    nova_coluna -= 1
                elif evento.key == pygame.K_RIGHT:
                    nova_coluna += 1

                if posicao_valida(nova_linha, nova_coluna):
                    pos_jogador = [nova_linha, nova_coluna]
                    if base.LABIRINTO[nova_linha][nova_coluna] in (2, 3, 4):
                        vitoria = True

        tela.fill(COR_FUNDO)
        desenhar_labirinto(tela)
        desenhar_jogador(tela, pos_jogador)
        pygame.display.flip()

        if vitoria:
            if base.fase_atual < len(base.FASES) - 1:
                # mostra a tela "Next Level" antes de seguir
                tela_proxima_fase()
                carregar_fase(base.fase_atual + 1)
                pos_jogador = base.encontrar_inicio()
                vitoria = False
            else:
                escolha = tela_final()
                if escolha == "reiniciar":
                    carregar_fase(0)
                    base.fase_atual = 0
                    pos_jogador = base.encontrar_inicio()
                    vitoria = False
                else:
                    rodando = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
