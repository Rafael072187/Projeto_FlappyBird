<center>
  <h1 style="font-size:2.4em; margin-bottom:0.1em;">🕹️ Projeto FlappyBird (Pygame + modo IA)</h1>
  <p style="margin-top:0.2em; font-size:1.05em; color:#555;">
    Implementação do Flappy Bird em Python com Pygame, incluindo um modo de experimento com algoritmo genético para jogar automaticamente.
  </p>
  <p>
    <a href="https://github.com/Rafael072187/Projeto_FlappyBird" style="background:#24292F;color:#fff;padding:8px 14px;border-radius:8px;text-decoration:none;font-weight:600;">
      🔗 Repositório no GitHub
    </a>
  </p>
</center>

<hr>

## 🧭 Tabela de Conteúdos
- Descrição  
- Instalação  
- Uso  
- Tecnologias  
- Como contribuir  
- Autor  
- Observações  

---

## 📘 Descrição
<details>
<summary><b>Resumo</b></summary>

Este projeto traz uma versão jogável do **Flappy Bird** escrita em **Python** usando **Pygame**. O foco é didático: o repositório contém um **modo manual** para você jogar e um **modo de experimento com algoritmo genético** que tenta aprender uma política simples para ultrapassar os canos.

A organização do repo indica três pontos principais:  
- `FlappyBird.py`: jogo clássico com renderização, física simples (gravidade/impulso), colisão com canos e base, contagem de pontos;  
- `ga.py`: experimento de **algoritmo genético** (GA) que executa episódios, avalia desempenho e evolui indivíduos (políticas de pulo) ao longo de gerações;  
- `run.py`: atalho/launcher para iniciar um dos modos.  
Há também uma pasta `imgs/` com os assets (bg, base, pipe, pássaro) usados na renderização do jogo. :contentReference[oaicite:0]{index=0}

Em suma: é um projeto para **estudar Pygame** (loop de jogo, sprites, colisão) e **experimentar IA evolutiva** em um ambiente 2D simples — bom material para portfólio e para aulas de introdução a jogos/IA.
</details>

---

## ⚙️ Instalação
<details>
<summary><b>Passo a passo (Linux / macOS / Windows)</b></summary>

1) **Clonar o repositório**
bash
git clone https://github.com/Rafael072187/Projeto_FlappyBird.git
cd Projeto_FlappyBird
Criar e ativar o ambiente virtual

bash
Copiar código
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
Instalar dependências mínimas

O projeto é 100% Python. O arquivo de requisitos não está explícito no repo, mas, pelo código e assets, o mínimo necessário é:

bash
Copiar código
pip install pygame numpy
Se o seu Python for muito novo, use pip install "pygame<2.6" ou instale via pacotes do sistema (Linux) antes.

</details>

---
🖥️ Uso
<details> <summary><b>Como usar o projeto (exemplos práticos)</b></summary>
1) Jogo manual (recomendado para começar)
Inicie o jogo clássico controlado pelo jogador:

bash
Copiar código
python FlappyBird.py
Controles típicos: barra de espaço ou clique para “bater asas”. Evite os canos; cada passagem conta pontos.
Assets de cenário e pássaro são carregados de imgs/ para compor o visual e as colisões (pipe/base/bg). 
GitHub

2) Modo IA (algoritmo genético)
Rode o experimento que tenta evoluir “o tempo de pulo”:

bash
Copiar código
python ga.py
O script executa diversas iterações (gerações), avalia a pontuação (fitness) de cada indivíduo e evolui a população. Ao final de cada geração, os melhores indivíduos são selecionados/mutados para a próxima rodada. Útil para ter intuição de como heurísticas evolutivas podem aprender comportamentos em jogos simples.

3) Launcher (se aplicável)
bash
Copiar código
python run.py
Use se você preferir um ponto único de entrada — normalmente abre menu/opções para escolher o modo (jogo manual ou GA).

</details> <p align="center" style="margin-top:14px;"> <img src="https://cdn-icons-png.flaticon.com/512/906/906343.png" width="90" alt="ícone ilustrativo"><br> <i>Representação simbólica. Faça screenshots do jogo rodando e adicione à pasta de imagens do repositório para ilustrar.</i> </p>

---
🛠️ Tecnologias
<details> <summary><b>Stack principal (com papéis)</b></summary>
Python 3.x — linguagem do projeto

Pygame — loop do jogo, renderização, input, colisões

NumPy — utilitários numéricos no GA (seleção, mutação, amostragem)

Assets locais (imgs/) — sprites do pássaro, canos, base e fundo

</details>

---
🤝 Como contribuir
<details> <summary><b>Guia rápido</b></summary>
Faça um fork do repositório

Crie uma branch:

bash
Copiar código
git checkout -b feature/nova-feature
Commits (use mensagens claras):

bash
Copiar código
git commit -m "feat: adiciona placar com recorde salvo"
git push origin feature/nova-feature
Abra um Pull Request explicando o que mudou, por quê e como testar.

Sugestões de contribuições úteis

Tela de menu/pause/game over mais caprichada

Ajuste fino da detecção de colisão (masks)

Persistência de recorde local (JSON/pickle)

Painel para visualizar evolução do GA (gráficos de fitness por geração)

Parametrizar GA por linha de comando (tamanho-pop, taxa de mutação, número de gerações)

</details>

---
👤 Autor
<details> <summary><b>Contatos</b></summary> <p> <b>Rafael Bittencourt de Araújo</b> — desenvolvedor do projeto.<br> GitHub: <a href="https://github.com/Rafael072187" target="_blank">github.com/Rafael072187</a> </p> </details>
📝 Observações
✅ Estágio atual: jogável localmente; modo GA para estudo/experimento.

---
🔧 Próximos passos sugeridos (prioridade)

Testes rápidos para garantir FPS estável e colisão robusta

Config externa (ex.: config.json) para velocidade, gap dos canos, gravidade, taxa de mutação

Headless GA (sem render) para treinar mais rápido e só renderizar top 1 da geração

Dockerfile ou conda env para reprodutibilidade
⚠️ Performance: rodar GA com render ligado pode ser lento; considere desativar render durante treino.

<p align="center" style="margin-top:18px;"> <a href="https://github.com/Rafael072187/Projeto_FlappyBird" style="background:#0b5fff;color:#fff;padding:10px 18px;border-radius:8px;text-decoration:none;font-weight:600;"> Ver repositório </a> </p> <p align="center" style="margin-top:14px;color:#666;"> Estrutura gerada a partir da análise dos arquivos e da árvore do repositório. </p>
