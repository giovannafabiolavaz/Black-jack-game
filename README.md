# Jogo 21 com Sockets UDP - Trabalho Prático de Redes

**Trabalho realizado por: Giovanna Fabíola Vaz e Luiza Rodrigues Vertelo**

## Descrição Geral
Este projeto é uma implementação do jogo de cartas **21 (Blackjack)** usando a linguagem **Python** e **sockets UDP** para comunicação entre cliente e servidor. 
Foi desenvolvido como trabalho prático da disciplina de **Redes de Computadores**, solicitado pelo professor **Lucas Bragança da Silva**.

O sistema é composto por dois programas principais:
- `servidor.py`: controla as partidas e gerencia os jogadores.
- `cliente.py`: interage com o jogador e participa das partidas.

## Como Executar

### 1. Clone o repositório (ou copie os arquivos):
```bash
https://github.com/giovannafabiolavaz/Black-jack-game.git
```

### 2. Execute o servidor:
```bash
python servidor.py
```

### 3. Execute o(s) cliente(s) em outro(s) terminal(is):
```bash
python cliente.py
```

Cada jogador deve digitar seu nome ao iniciar o cliente.

## Protocolo de Comunicação
A comunicação entre cliente e servidor é feita por mensagens **textuais via UDP**. As mensagens seguem um protocolo simples:

| Comando | Origem | Função |
|--------|--------|--------|
| `ENTRAR:<nome>` | Cliente → Servidor | Solicita entrada no jogo |
| `PEDIR_CARTA` | Cliente → Servidor | Solicita nova carta |
| `PARAR` | Cliente → Servidor | Finaliza jogada |
| `CARTA:<valor>` | Servidor → Cliente | Envia carta sorteada |
| `MENSAGEM:<texto>` | Servidor → Cliente | Mensagem informativa |
| `RESULTADO:<ganhou/perdeu>` | Servidor → Cliente | Resultado final da rodada |

## Regras do Jogo
- Cada jogador pode solicitar cartas até atingir ou ultrapassar **21 pontos**.
- Se ultrapassar 21, o jogador perde automaticamente.
- O jogador pode **parar** a qualquer momento.
- A rodada termina quando todos os jogadores **pararem** ou **estourarem**.
- O servidor avalia os pontos e informa o resultado aos jogadores.

## Funcionalidades
### Servidor:
- Gerencia múltiplos jogadores via UDP
- Sorteia cartas e calcula pontuações
- Avalia resultados ao fim da rodada
- Envia mensagens de feedback

### Cliente:
- Permite entrada com nome
- Mostra cartas recebidas e pontuação
- Permite pedir carta ou parar
- Exibe o resultado da rodada

## 🔧 Tecnologias Utilizadas
- Python 3.10+
- Biblioteca padrão `socket` para comunicação UDP

## Estrutura do Projeto
```
Black-jack-game/
├── servidor.py
├── cliente.py
└── README.md
```

## Sugestões de Teste
- Abrir um terminal e rodar `servidor.py`
- Abrir dois outros terminais e rodar dois `cliente.py` diferentes
- Jogar uma rodada para observar as interações e mensagens trocadas
