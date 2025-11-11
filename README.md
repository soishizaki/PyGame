# Maze Kitty: Treasure Hunt 

Jogo 2D em Python onde você controla um gatinho em um labirinto, tentando chegar à saída antes do tempo acabar.

## 🕹️ Como jogar

- Use as **setas do teclado** para mover o gatinho:
  - ⬆ ⬇ ⬅ ➡ para andar pelo labirinto.
- Seu objetivo é **chegar à saída/tesouro** em cada fase.
- Cada fase tem um **tempo limite** de 30 segundos.
- Se o tempo zerar, você **volta para a Fase 1**.
- Atalhos:
  - `ESC` fecha o jogo  
  - `ENTER` ou `ESPAÇO` confirmam botões nas telas  
  - `I` no menu inicial abre a tela de **instruções (Info)**

## ▶️ Como iniciar o jogo

1. Tenha **Python 3** instalado.
2. Instale o **Pygame**:
   pip install pygame
3. Execute o arquivo jogo.py

## Demonstração do jogo em vídeo
Link do YouTube:
https://youtu.be/Zi8IEtKEet8?si=awwFUbdwy8c-gcvO

## Fontes
- Tiles: 
    https://github.com/Insper/pygame-snippets/blob/master/img/tile-wood.png
    https://github.com/Insper/pygame-snippets/blob/master/img/tile-grass.png
- Kitty: gerado pelo chatGPT 5
- Telas de informação, início, fim, próxima fase: geradas pelo chatGPT 5
- Tesouros: gerados pelo chatGPT 5
- Sons: https://freesound.org/


## Uso de IAs generativas

- As lista de cores das estrelas nas páginas de vitória foi gerada pelo chatGPT 5.:

CORES_ESTRELAS = [
    (255, 255, 0),   
    (255, 192, 203), 
    (135, 206, 250), 
    (144, 238, 144), 
    (255, 165, 0),   
    (255, 255, 255)  
]

- A função criar_estrela foi 80% gerada pelo chatGPT 5:

def criar_estrela(multicolor=False):
    cor = random.choice(CORES_ESTRELAS) if multicolor else (255, 255, 0)
    return {
        "x": random.randint(0, LARGURA_TELA),
        "y": random.randint(-ALTURA_TELA, 0),
        "vel": random.uniform(1.5, 4.0),
        "raio": random.randint(2, 4),
        "cor": cor
    }

- Os loops das animações das estrelas foram 80% gerados pelo chatGPT 5:

for e in estrelas:
    e["y"] += e["vel"]
    if e["y"] > ALTURA_TELA + 10:
        novo = criar_estrela()
        e["x"] = novo["x"]
        e["y"] = novo["y"]
        e["vel"] = novo["vel"]
        e["raio"] = novo["raio"]

for e in estrelas:
    e["y"] += e["vel"]
    if e["y"] > ALTURA_TELA + 10:
        novo = criar_estrela(multicolor=True)
        e["x"], e["y"], e["vel"], e["raio"], e["cor"] = \
            novo["x"], novo["y"], novo["vel"], novo["raio"], novo["cor"]

for e in estrelas:
    pygame.draw.circle(
        tela,
        e["cor"],
        (int(e["x"]), int(e["y"])),
        e["raio"]
    )


