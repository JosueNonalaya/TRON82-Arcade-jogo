# TRON82-Arcade-jogo

## Definição:
Este projeto consiste em uma implementação de um jogo baseado no clássico conceito das motos de luz de **TRON(1982)**. Será desenvolvido em Python utilizando a biblioteca Pygame.

O jogo tem como objetivo proporcionar uma experiência arcade na qual os jogadores controlam motocicletas que deixam um rastro permanente pela arena. O jogador deve utilizar sua velocidade e capacidade de antecipação para evitar colisões com as paredes, com os rastros existentes e com os demais jogadores.

O projeto está sendo desenvolvido também como uma forma de estudo e aplicação prática de conceitos de **Programação Orientada a Objetos, arquitetura de software, padrões de projeto e desenvolvimento de jogos**.

Entre as funcionalidades planejadas estão:
- Menu principal.
- Seleção do modo de jogo.
- Partida entre dois jogadores. 
- Partida entre jogador e computador.
- Sistema de pontuação.
- Salvar maiores pontuações.
- Configurações da partida(som, musica, cores das motos).
- Pausa e reinicialização da partida.


## Tecnologias Utilizadas

- Linguagem e Libs:
	- Python 3.10+
	- Pygame

- Ferramentas:
	- IntelliJ IDEA
	- PowerShell
	- GitHub
	- Ambiente virtual Python (`venv`)
	- Astah
	- VisualParadigm Community Edition

---
## Conceitos aplicados

##### POO - Programação Orientada a Objetos
- Organiza o sistema por meio de objetos que possuem dados(atributos) e comportamentos(metodos), representando elementos do jogo

- Entre as principais entidades estão:
	1. **Player**(nome,tipo,moto associada)
	2. **LightCycle**(posicao, cor, estado)
	3. **GameBoard**(limites,posicoes_ocupadas)
	4. **Score** representa e controla pontuação.

##### Clean Architecture
- Organiza o jogo em camadas, mantem as regras principais independentes de tecnologias externas, neste caso o pygame.(organiza responsabilidades)

##### State Pattern
- Permite que um objeto altere o seu comportamento com seu estado atual. Será utilizado para poder mudar o estados como Menu, Partida, Pausa.(controla o fluxo do jogo)

##### Strategy Pattern
- Permite trocar o comportamento de um objeto sem modificar a classe o u sua propria estrutura.(troca entre Humano vs CPU)

---
## Estrutura de Pastas

A estrutura planejada do projeto está organizada por responsabilidade:

1. **entities**: Contém as principais entidades do domínio do jogo, como *Jogador* e *LightCycle*.

2. **game**: Contém as regras e componentes responsáveis pelo funcionamento da partida, como *Tabuleiro* e a lógica do jogo

3. **controllers**: Tem as diferentes estratégias de controle das *LightCycle*, controle por teclado ou CPU.

4. **views**: Contém as diferentes telas do programa, interface grafica.

5. **servicos**: Contém funcionalidades auxiliares que não pertencem diretamente ao domínio do jogo(gerenciar musica e efeitos).

6. **assets**: Os recursos usados pela aplicação, imgs, efeitos, fontes.

7.  **config**: Guarda configurações que o sistema ira usar.

---
## UML

Durante a evolução do projeto serão desenvolvidos diagramas UML para representar sua arquitetura e suas relações.

Entre os diagramas planejados estão:

- Diagrama de classes.
    
- Diagrama de estados.
	
- Diagrama de casos de uso.

Os diagramas serão atualizados conforme a arquitetura do projeto evoluir.

---
## Diario de Bordo
### Sprint 1 (07/09/26) — Clean Architecture

Nesta sprint, foi feito uma refatoração para melhorar a separação de responsabilidades e facilitar a evolução. A lógica principal do jogo foi dividida em componentes independentes, separando entidades (Player e LightCycle), as regras do tabuleiro (Board), o controle dos jogadores (Controller, Humano e CPU) e o renderização (Renderizado). O tron_lightcycles.py passou a atuar principalmente como orquestrador do fluxo do jogo, enquanto as responsabilidades visuais foram removidas dele.
