import pygame
import os
import random
import sys
import time

# -------------------------
# CONFIGURAÇÕES
# -------------------------
TELA_LARGURA = 500
TELA_ALTURA = 800
DELAY_REINICIAR = 3  # ajuste livre


# -------------------------
# CARREGAMENTO DE IMAGENS
# -------------------------
IMAGEM_CANO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
IMAGEM_TERRENO = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
IMAGEM_BACKGROUND = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
IMAGENS_PASSARO = [
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png'))),
]

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 40)


# -------------------------
# CLASSE PASSARO
# -------------------------
class Passaro:
    IMGS = IMAGENS_PASSARO
    ROTACAO_MAXIMA = 25
    VELOCIDADE_ROTACAO = 20
    TEMPO_ANIMACAO = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagem_imagem = 0
        self.imagem = self.IMGS[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.ROTACAO_MAXIMA:
                self.angulo = self.ROTACAO_MAXIMA
        else:
            if self.angulo > -90:
                self.angulo -= self.VELOCIDADE_ROTACAO

    def desenhar(self, tela):
        self.contagem_imagem += 1

        if self.contagem_imagem < self.TEMPO_ANIMACAO:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.TEMPO_ANIMACAO * 4:
            self.imagem = self.IMGS[1]
        else:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.TEMPO_ANIMACAO * 2

        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro = self.imagem.get_rect(topleft=(self.x, self.y)).center
        rect = imagem_rotacionada.get_rect(center=pos_centro)
        tela.blit(imagem_rotacionada, rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


# -------------------------
# CLASSE CANO
# -------------------------
class Cano:
    DISTANCIA = 200
    VELOCIDADE = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
        self.CANO_BASE = IMAGEM_CANO
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.CANO_TOPO.get_height()
        self.pos_base = self.altura + self.DISTANCIA

    def mover(self):
        self.x -= self.VELOCIDADE

    def desenhar(self, tela):
        tela.blit(self.CANO_TOPO, (self.x, self.pos_topo))
        tela.blit(self.CANO_BASE, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
        base_mask = pygame.mask.from_surface(self.CANO_BASE)

        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))

        topo_hit = passaro_mask.overlap(topo_mask, distancia_topo)
        base_hit = passaro_mask.overlap(base_mask, distancia_base)

        return topo_hit or base_hit


# -------------------------
# CLASSE TERRENO
# -------------------------
class Terreno:
    VELOCIDADE = 5
    LARGURA = IMAGEM_TERRENO.get_width()
    IMAGEM = IMAGEM_TERRENO

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.LARGURA

    def mover(self):
        self.x1 -= self.VELOCIDADE
        self.x2 -= self.VELOCIDADE

        if self.x1 + self.LARGURA < 0:
            self.x1 = self.x2 + self.LARGURA
        if self.x2 + self.LARGURA < 0:
            self.x2 = self.x1 + self.LARGURA

    def desenhar(self, tela):
        tela.blit(self.IMAGEM, (self.x1, self.y))
        tela.blit(self.IMAGEM, (self.x2, self.y))


# -------------------------
# DESENHAR TELA
# -------------------------
def desenhar_tela(tela, passaros, canos, terreno, pontos):
    tela.blit(IMAGEM_BACKGROUND, (0, 0))
    for cano in canos:
        cano.desenhar(tela)
    terreno.desenhar(tela)
    for passaro in passaros:
        passaro.desenhar(tela)

    texto = FONTE_PONTOS.render(f"Pontos: {pontos}", True, (255, 255, 255))
    tela.blit(texto, (10, 10))

    pygame.display.update()


# -------------------------
# GAME OVER
# -------------------------
def mostrar_game_over(tela):
    texto = FONTE_PONTOS.render("💀 GAME OVER 💀", True, (255, 0, 0))
    tela.blit(texto, (
        (TELA_LARGURA - texto.get_width()) // 2,
        (TELA_ALTURA - texto.get_height()) // 2,
    ))
    pygame.display.update()
    time.sleep(DELAY_REINICIAR)


# -------------------------
# MODO NORMAL
# -------------------------
def jogar_normal():
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))

    while True:  # reinicia infinitamente
        passaros = [Passaro(230, 350)]
        terreno = Terreno(730)
        canos = [Cano(700)]
        pontos = 0
        relogio = pygame.time.Clock()

        rodando = True
        while rodando:
            relogio.tick(30)

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                    passaros[0].pular()

            for p in passaros:
                p.mover()
            terreno.mover()

            adicionar_cano = False
            remover = []

            for cano in canos:
                for p in passaros:
                    if cano.colidir(p):
                        mostrar_game_over(tela)
                        rodando = False
                        break

                    if not cano.passou and p.x > cano.x:
                        cano.passou = True
                        pontos += 1
                        adicionar_cano = True

                cano.mover()
                if cano.x + cano.CANO_BASE.get_width() < 0:
                    remover.append(cano)

            if adicionar_cano:
                canos.append(Cano(600))

            for c in remover:
                canos.remove(c)

            for p in passaros:
                if p.y > terreno.y or p.y < 0:
                    mostrar_game_over(tela)
                    rodando = False

            desenhar_tela(tela, passaros, canos, terreno, pontos)


# -------------------------
# START DIRETO
# -------------------------
if __name__ == "__main__":
    jogar_normal()
