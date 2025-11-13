from FlappyBird import jogar_normal
from ga import treinar_ga

ALGORITMO = "GA"   # GA | NONE
POP = 50
GERACOES = 30
MOSTRAR_TREINO = True


def main():
    if ALGORITMO == "GA":
        treinar_ga(populacao_tam=POP, geracoes=GERACOES, mostrar=MOSTRAR_TREINO)

    elif ALGORITMO == "NONE":
        jogar_normal()

    else:
        print("Algoritmo desconhecido! Use GA ou NONE.")


if __name__ == "__main__":
    main()
