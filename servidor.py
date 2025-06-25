import socket
import threading
import random

# Define o host e a porta que o servidor irá escutar
host = 'localhost'
port = 12345

# Criação do socket UDP
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((host, port))  # Faz o bind na porta e host definidos

# Dicionário que armazena os dados de cada jogador conectado
# Estrutura: {endereço: {'nome': str, 'cartas': list[int], 'pontuacao': int, 'ativo': bool}}
jogadores = {}

# Função para sortear uma carta (valores de 1 a 10)
def distribui_carta():
    return random.randint(1, 10)

# Avalia os jogadores ao final da partida
def avalia_jogadores():
    resultados = {}
    for enderço, dados in jogadores.items():
        if dados['pontuacao'] > 21:
            resultados[enderço] = 'perdeu'  # Estourou
        else:
            # Define a maior pontuação entre os jogadores que não estouraram
            maior = max([v['pontuacao'] for v in jogadores.values() if v['pontuacao'] <= 21], default=0)
            resultados[enderço] = 'ganhou' if dados['pontuacao'] == maior else 'perdeu'
    return resultados

# Envia uma mensagem textual ao cliente (endereço)
def envia_mensagem(endereco, mensagem):
    servidor.sendto(mensagem.encode(), endereco)

# Trata as mensagens recebidas de cada cliente
def trata_mensagem(mensagem, endereco):
    # Primeiro contato do cliente → ENTRAR:<nome>
    if endereco not in jogadores and mensagem.startswith("ENTRAR:"):
        nome = mensagem.split(":")[1]
        jogadores[endereco] = {
            'nome': nome,
            'cartas': [],
            'pontuacao': 0,
            'ativo': True
        }
        envia_mensagem(endereco, f"MENSAGEM:Bem-vindo {nome}!")

    # Cliente solicita nova carta
    elif mensagem == "PEDIR_CARTA":
        if not jogadores[endereco]['ativo']:
            envia_mensagem(endereco, "MENSAGEM:Você já finalizou sua jogada.")
            return

        carta = distribui_carta()
        jogadores[endereco]['cartas'].append(carta)
        jogadores[endereco]['pontuacao'] += carta
        envia_mensagem(endereco, f"CARTA: {carta}")

        # Se estourar (pontuação > 21), jogador é desativado
        if jogadores[endereco]['pontuacao'] > 21:
            jogadores[endereco]['ativo'] = False
            envia_mensagem(endereco, f"MENSAGEM:Você estourou! Pontuação {jogadores[endereco]['pontuacao']}")

    # Cliente decide parar de jogar
    elif mensagem == "PARAR":
        jogadores[endereco]['ativo'] = False
        envia_mensagem(endereco, f"MENSAGEM:Você parou com {jogadores[endereco]['pontuacao']} pontos.")

# Loop principal do servidor: recebe e processa mensagens
def monitor():
    while True:
        dados, endereco = servidor.recvfrom(1024)  # Aguarda mensagem de cliente
        mensagem = dados.decode()
        trata_mensagem(mensagem, endereco)

        # Condição de fim de rodada: todos os jogadores já pararam ou estouraram
        if len(jogadores) >= 2 and all(not j['ativo'] for j in jogadores.values()):
            resultados = avalia_jogadores()
            for end, res in resultados.items():
                envia_mensagem(end, f"RESULTADO:{res}")
            break  # Encerra a partida após enviar os resultados

# Inicia o servidor
print("Servidor aguardando jogadores...")
monitor()
