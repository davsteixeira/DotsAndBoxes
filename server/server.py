import socket
import threading
from watchdog import Watchdog
from tabuleiro import Tabuleiro

localIP = "localhost"
localPort = 1111
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

timeout = 60
wd = Watchdog(timeout)

lin_tab = 5
col_tab = 4

fila_espera = []
addresses = []

play_again_addresses = []
play_again_names = []

win_award_points: int = 3

# Dicionário para armazenar as partidas ativas
active_games = {}
game_id_counter = 0



def add_fila(nome, endereco):
    fila_espera.append(nome)
    addresses.append(endereco)
    print(f"Jogador {nome} entrou na fila de espera.")


def send_msg(msg, address):
    UDPServerSocket.sendto(str.encode(msg), address)


def send_all(msg, address_list):
    for addr in address_list:
        send_msg(msg, addr)

def receive_msg(cod, address):
    UDPServerSocket.sendto(str.encode(cod), address)

    wd.start()

    addrs = wd.get_addresses()
    names = wd.get_names()

    player_name = ""
    if address == addrs[0]:
        player_name = names[0]
    elif address == addrs[1]:
        player_name = names[1]

    wd.set_player(address, player_name)

    bytes_adress_pair = UDPServerSocket.recvfrom(bufferSize)
    wd.refresh()
    resposta = bytes_adress_pair[0]

    wd.stop()
    
    send_resposta = resposta.decode()
    
    return send_resposta


def update_scoreboard(winner_name):
    # Lógica para atualizar o placar do vencedor
    with open("scoreboard.txt", "a") as file:
        file.write(f"{winner_name} - {win_award_points} pontos\n")


def handle_rematch(game_id):
    # Lógica para permitir o rematch ou encerrar a partida
    pass


def run_game(addresses, names):
    global game_id_counter
    # Gerar um ID único para a partida
    game_id = game_id_counter
    game_id_counter += 1

    # Criar uma instância de Tabuleiro para essa partida
    tab = Tabuleiro(lin_tab, col_tab)
    
    # Registrar jogadores e seus endereços na partida
    tab.addresses_management(addresses[0], addresses[1])
    wd.set_addresses(addresses[0], addresses[1])
    wd.set_names(names[0], names[1])

    active_games[game_id] = {
        'tab': tab,
        'players': addresses,
        'names': names,
        'status': 'in_progress'
    }

    # Enviar mensagem para os jogadores
    UDPServerSocket.sendto(str.encode("Jogo Iniciando...\n"), addresses[0])
    UDPServerSocket.sendto(str.encode("Jogo Iniciando...\n"), addresses[1])

    winner = tab.game()

    winner_name = "draw"  # Default
    if winner == addresses[0]:
        winner_name = names[0]
    elif winner == addresses[1]:
        winner_name = names[1]

    # Atualizar o placar se houver vencedor
    if winner_name != "draw":
        update_scoreboard(winner_name)

    # Adicionar lógica para permitir que a partida seja jogada novamente, se necessário
    handle_rematch(game_id)


def main():
    global fila_espera, addresses, play_again_addresses, play_again_names

    while True:
        # Adiciona jogadores na fila de espera
        while len(fila_espera) < 2:
            print(f"A fila de espera possui {len(fila_espera)} jogadores")
            print("Aguardando conexão de jogadores ...")

            # Envia mensagem de status da fila para jogadores em espera
            send_all(f"Há {len(fila_espera)} jogador(s) na fila, verificando entrada de novos jogadores...\n", addresses)

            # Espera por uma nova mensagem do cliente
            bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
            message = bytesAdressPair[0]
            address = bytesAdressPair[1]
            decodedmsg = message.decode()
            data = decodedmsg.split(":")

            if data[0] == "1":
                add_fila(data[1], address)
                send_msg("O jogo só iniciará com 2 jogadores em espera!\n", address)
            elif data[0] == "2":
                read_db = open("scoreboard.txt", "r")
                content_socoreboard = read_db.readlines()
                for line in content_socoreboard:
                    send_msg(line, address)
                send_msg("scoreboard_end", address)

        # Quando 2 jogadores entram na fila, cria-se uma nova thread para o jogo
        addresses_pair = addresses[:2]  # Pega os dois primeiros jogadores
        names_pair = fila_espera[:2]

        # Inicia a thread para o jogo
        game_thread = threading.Thread(target=run_game, args=(addresses_pair, names_pair))
        game_thread.start()

        # Remove os jogadores da fila de espera
        fila_espera = fila_espera[2:]
        addresses = addresses[2:]

        # O servidor continua ouvindo novas conexões




if __name__ == "__main__":
    UDPServerSocket.bind((localIP, localPort))
    print(f"Servidor iniciado em {localIP}:{localPort}")
    main()

