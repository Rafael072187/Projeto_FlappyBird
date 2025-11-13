import random
import math
import pygame
from FlappyBird import Passaro, Cano, Terreno, desenhar_tela, TELA_ALTURA, TELA_LARGURA


# =======================================================
#   REDE NEURAL SIMPLES (1 hidden layer: 3 neurônios)
# =======================================================

class RedeNeural:
    def __init__(self):
        # pesos aleatórios
        self.w1 = [[random.uniform(-1, 1) for _ in range(3)] for _ in range(3)]
        self.w2 = [random.uniform(-1, 1) for _ in range(3)]

    def ativacao(self, x):
        return 1 / (1 + math.exp(-x))  # sigmoid

    def forward(self, x):
        hidden = [0, 0, 0]
        for i in range(3):
            hidden[i] = self.ativacao(
                x[0] * self.w1[i][0] +
                x[1] * self.w1[i][1] +
                x[2] * self.w1[i][2]
            )

        out = sum(hidden[i] * self.w2[i] for i in range(3))
        return out  # >0 => pular


# =======================================================
#            GENETIC ALGORITHM — PÁSSARO
# =======================================================

class Individuo:
    def __init__(self):
        self.rede = RedeNeural()
        self.fitness = 0


# =======================================================
#            FUNÇÕES DO GA
# =======================================================

def mutar(rede, taxa=0.1):
    # mutação leve dos pesos
    for i in range(3):
        for j in range(3):
            if random.random() < taxa:
                rede.w1[i][j] += random.uniform(-0.2, 0.2)

    for i in range(3):
        if random.random() < taxa:
            rede.w2[i] += random.uniform(-0.2, 0.2)


def cruzar(pai, mae):
    filho = Individuo()

    # mistura metade dos pesos do pai e da mãe
    for i in range(3):
        for j in range(3):
            filho.rede.w1[i][j] = random.choice([pai.rede.w1[i][j], mae.rede.w1[i][j]])

    for i in range(3):
        filho.rede.w2[i] = random.choice([pai.rede.w2[i], mae.rede.w2[i]])

    return filho


# =======================================================
#         EXECUTAR UMA GERAÇÃO DE TREINAMENTO
# =======================================================

def rodar_geracao(populacao, mostrar=False):
    pygame.init()
    tela = pygame.display.set_mode((TELA_LARGURA, TELA_ALTURA))

    passaros = [Passaro(230, 350) for _ in populacao]
    terreno = Terreno(730)
    canos = [Cano(700)]

    clock = pygame.time.Clock()
    pontos = 0
    vivos = len(passaros)

    while vivos > 0:
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        # escolher cano alvo
        cano_alvo = canos[0]
        if len(canos) > 1 and passaros[0] and passaros[0].x > canos[0].x + canos[0].CANO_TOPO.get_width():
            cano_alvo = canos[1]

        # mover pássaros
        for i, passaro in enumerate(passaros):
            if passaro is None:
                continue

            estado = [
                (cano_alvo.x - passaro.x) / 500,
                (passaro.y - cano_alvo.altura) / 500,
                (passaro.y - cano_alvo.pos_base) / 500
            ]

            saida = populacao[i].rede.forward(estado)

            if saida > 0:
                passaro.pular()

            passaro.mover()
            populacao[i].fitness += 0.1

        terreno.mover()

        # colisões
        for i, passaro in enumerate(passaros):
            if passaro is None:
                continue

            for cano in canos:
                if cano.colidir(passaro):
                    passaros[i] = None
                    vivos -= 1
                    break

            if passaro is None:
                continue

            if passaro.y < 0 or passaro.y > terreno.y:
                passaros[i] = None
                vivos -= 1

        # novo cano
        adicionar = False
        for cano in canos:
            for passaro in passaros:
                if passaro is None:
                    continue

                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    pontos += 1
                    adicionar = True

                    for ind in populacao:
                        ind.fitness += 5
                    break

        if adicionar:
            canos.append(Cano(600))

        canos = [c for c in canos if c.x + c.CANO_TOPO.get_width() > 0]

        for c in canos:
            c.mover()

        # desenhar SEMPRE quando mostrar=True
        if mostrar:
            vivos_para_desenhar = [p for p in passaros if p]
            if not vivos_para_desenhar:
                vivos_para_desenhar = []  # sem pássaros
            desenhar_tela(tela, vivos_para_desenhar, canos, terreno, pontos)

    return pontos


# =======================================================
#              LOOP EVOLUTIVO PRINCIPAL
# =======================================================

def treinar_ga(populacao_tam=50, geracoes=50, mostrar=False):
    populacao = [Individuo() for _ in range(populacao_tam)]

    for g in range(geracoes):
        print(f"\n🔵 Geração {g+1}/{geracoes}")

        pontos = rodar_geracao(populacao, mostrar)

        print(f"🏆 Melhor pontuação da geração: {pontos}")

        # seleção — pega top 20%
        populacao.sort(key=lambda ind: ind.fitness, reverse=True)
        elite = populacao[:populacao_tam // 5]

        # nova geração
        nova_pop = elite.copy()
        while len(nova_pop) < populacao_tam:
            pai = random.choice(elite)
            mae = random.choice(elite)
            filho = cruzar(pai, mae)
            mutar(filho.rede)
            nova_pop.append(filho)

        populacao = nova_pop

    print("\n🎉 Treinamento GA finalizado!")
    return populacao
