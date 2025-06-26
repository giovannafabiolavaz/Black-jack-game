import socket  # Importa a biblioteca de sockets para comunicação em rede

# Define o host (localhost para teste local) e porta do servidor
host = 'localhost'
port = 12345

# Cria o socket UDP do cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Solicita o nome do jogador e envia a mensagem de entrada ao servidor
nome = input("Digite seu nome: ")
cliente.sendto(f"ENTRAR:{nome}".encode(), (host, port))

# Loop principal de interação com o jogador
while True:
    # Exibe o menu de opções
    print("\nEscolha uma opção:")
    print("1 - Pedir carta")
    print("2 - Parar")
    opcao = input("Opção: ")

    # Envia o comando correspondente ao servidor
    if opcao == "1":
        cliente.sendto("PEDIR_CARTA".encode(), (host, port))
    elif opcao == "2":
        cliente.sendto("PARAR".encode(), (host, port))
        break  # Encerra o envio após o jogador parar

    # Aguarda resposta do servidor com timeout
    try:
        cliente.settimeout(5)  # Define tempo máximo de espera por resposta (5 segundos)
        resposta, _ = cliente.recvfrom(1024)
        msg = resposta.decode()
        print("Servidor:", msg)

        # Sai do loop caso receba resultado final ou mensagem de estouro
        if "RESULTADO" in msg or "Você estourou" in msg:
            break
    except socket.timeout:
        print("Servidor não respondeu a tempo.")
        break

# Segunda parte: continua aguardando o resultado final se ainda não tiver sido recebido
while True:
    try:
        resposta, _ = cliente.recvfrom(1024)
        msg = resposta.decode()
        print("Servidor:", msg)
        if "RESULTADO" in msg:
            break  # Encerra o cliente após receber o resultado
    except socket.timeout:
        break  # Finaliza se não houver mais mensagens
