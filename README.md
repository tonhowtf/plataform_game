Um jogo de plataforma clássico desenvolvido com 💻 **Python + PGZero**, onde você controla um herói intrépido, desvia de obstáculos traiçoeiros, coleta moedas brilhantes e explora diversas fases desafiadoras!

---

## ✨ Sobre o Projeto

O objetivo principal é guiar o personagem através de múltiplas fases, cada uma com seus próprios desafios, inimigos e perigos. O jogo implementa mecânicas como movimentação baseada em física (gravidade), pulos, um sistema de "dash" (impulso), vidas limitadas, coleta de moedas e progressão por diferentes estágios. Foi cuidadosamente criado para atender a um conjunto específico de requisitos e demonstrar boas práticas de codificação em Pygame Zero.

---

## 🛠️ Tecnologias Utilizadas

-   **Python 3.x** (Recomenda-se Python 3.7 ou mais recente)
-   **PGZero (Pygame Zero)** - (A biblioteca Pygame é instalada automaticamente como uma dependência do PGZero) 

---

## 🎮 Controles

| Tecla / Ação        | Função                                           |
|---------------------|--------------------------------------------------|
| Seta Esquerda (`←`) | Mover o personagem para a esquerda               |
| Seta Direita (`→`)  | Mover o personagem para a direita                |
| Tecla `Z`           | Pular (funciona apenas quando o personagem está no chão)         |
| Tecla `X`           | Dash/Impulso (funciona quando o personagem está no ar e possui dashes disponíveis)       |
| Clique do Mouse     | Interagir com os botões nas telas de menu e outras interfaces clicáveis   |

---

## 💡 Mecânicas Principais

O jogo é construído em torno das seguintes mecânicas centrais:

* **Sistema de Vidas:** O jogador começa com 3 vidas. Ao colidir com um inimigo ou obstáculo perigoso, uma vida é perdida. Perder todas as vidas resulta em "Game Over".
* **Habilidade de Dash:** O personagem pode executar um impulso rápido no ar (3 dashes disponíveis por vida ou por entrada na fase).
* **Progressão por Fases:** O jogo é composto por uma sequência de fases (definidas como `MAP0` até `MAP4` no código), cada uma com um design de nível único, incluindo plataformas, obstáculos e inimigos.
* **Inimigos e Obstáculos:**
    * **Abelhas (`Bee`):** Inimigos que patrulham uma área específica.
    * **Espinhos (`obstacles/o2`):** Obstáculos estáticos que causam dano ao jogador.
* **Coleta de Moedas (`Coin`):** Moedas estão espalhadas pelas fases e podem ser coletadas pelo jogador, acompanhadas de um efeito sonoro.
* **Transição de Cenas:** O jogo flui através de várias cenas: Menu Principal, Tela de Introdução com a história, a Cena do Jogo em si, e uma Tela de Game Over (com mensagens diferentes para vitória ou derrota).
* **Animações de Sprite Detalhadas:** O personagem principal possui animações para diferentes estados (parado, andando para esquerda/direita, pulando, usando dash). Os inimigos também possuem animações.
* **Música e Efeitos Sonoros:** O jogo conta com música de fundo temática para diferentes momentos (menu, jogo, vitória, derrota) e efeitos sonoros para ações importantes como pulo, dash, coleta de moeda, e ao perder uma vida.
* **Física de Plataforma:** Implementa gravidade, detecção de colisão com plataformas para permitir que o personagem pouse e se mova sobre elas.

---

## 🧠 Como Rodar o Projeto

1.  **Pré-requisitos:**
    * Certifique-se de ter o **Python 3.7+** (ou uma versão mais recente compatível com PGZero) instalado em seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/).

2.  **Configuração do Projeto:**
    * Clone este repositório
    * Certifique-se de que todas as pastas de assets (como `images`, `sounds`, `music` contendo as subpastas `player`, `obstacles`, `titles`, `menu`, etc.) estejam na mesma estrutura que o código espera.

3.  **Instalação das Dependências:**
    * Abra um terminal ou prompt de comando.
    * Navegue até a pasta raiz do projeto (onde o arquivo `main.py` está localizado).
    * Instale a biblioteca PGZero. Isso também instalará o Pygame automaticamente se ainda não estiver presente:
        ```bash
        pip install pgzero ou pip install -r requeriments.txt
        ```

4.  **Executando o Jogo:**
    * Ainda no terminal, na pasta do projeto, execute o jogo usando o seguinte comando (assumindo que seu arquivo principal se chama `main.py`, conforme o contexto da nossa conversa):
        ```bash
        pgzrun main.py
        ```

---

