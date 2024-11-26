import socket
from watchdog import Watchdog
from tabuleiro import Tabuleiro

#"localhost" deve ser mudado para o endereço de ip da maquina do servidor
localIP = "localhost"
localPort = 1111
bufferSize = 1024

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

timeout = 60
wd = Watchdog(timeout)

lin_tab = 3
col_tab = 2

fila_espera = []
addresses = []

play_again_addresses = []
play_again_names = []

win_award_points: int = 3

def add_fila(msg, addr : tuple):

    fila_espera.append(msg)
    addresses.append(addr)
    print(f"Jogador \"{msg}\", do endereço {addr} foi adicionado a fila de espera")

def main():
    fila_espera.clear()
    addresses.clear()
    for nomes in play_again_names:
        fila_espera.append(nomes)
    for enderecos in play_again_addresses:
        addresses.append(enderecos)


    while len(fila_espera) < 2:

        print(f"A fila de espera possui {len(fila_espera)} jogadores")
        print("Aguardando conexão de jogadores ...")

        send_all(f"Há {len(fila_espera)} jogador na fila, verificando entrada de novos jogadores...\n", addresses)

        bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAdressPair[0]
        address = bytesAdressPair[1]

        decodedmsg = message.decode()
        data = decodedmsg.split(":")

        if data[0] == "1":
            add_fila(data[1], address)
            send_msg("O jogo só iniciará com 2 jogador em espera!\n", address)
        elif data[0] == "2":
            read_db = open("scoreboard.txt", "r")
            content_socoreboard = read_db.readlines()
            for line in content_socoreboard:
                send_msg(line,address)
            send_msg("scoreboard_end",address)

    tab = Tabuleiro(lin_tab, col_tab)

    tab.addresses_management(addresses[0],addresses[1])
    wd.set_addresses(addresses[0],addresses[1])
    wd.set_names(fila_espera[0],fila_espera[1])

    UDPServerSocket.sendto(str.encode("Jogo Ininicando...\n"), addresses[0])
    UDPServerSocket.sendto(str.encode("Jogo Ininicando...\n"), addresses[1])

    print(addresses)
    winner = tab.game()
    
    #winner = addresses[0]

    winner_name : str

    if winner == addresses[0]:
        winner_name = fila_espera[0]
    elif winner == addresses[1]:
        winner_name = fila_espera[1]
    else:
        winner_name = "draw"

    if winner_name != "draw":
        try:
            create_db = open("scoreboard.txt", "x")
            print("New scoreboard created!")
        except FileExistsError:
            pass
        edit_db = open("scoreboard.txt", "a")
        read_db = open("scoreboard.txt", "r")
        content = read_db.readlines()
        content_line = -1
        i = -1
        for line in content:
            i += 1
            content_data = content[i].split(" : ")
            if content_data[0] == winner:
                content_line = i
                final_points = int(content_data[1]) + win_award_points
                content[i] = f"{winner} : {final_points}\n"
                rewrite_db = open("scoreboard.txt", "w")
                rewrite_db.writelines(content)
                rewrite_db.close()
                break
        if content_line == -1:
            edit_db.write(f"{winner} : {win_award_points}\n")
        read_db.close()
        edit_db.close()

def send_all(msg,players_addr):
    for addr in players_addr:
        UDPServerSocket.sendto(str.encode(msg), addr)

def send_msg(msg, address):
    UDPServerSocket.sendto(str.encode(msg), address)

def recieve_msg(cod, address):
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

def play_again():
    j = 0
    for i in addresses:
        send_msg("play_again", addresses[j])
        bytesAdressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAdressPair[0]

        if message.decode() == "play_again_positive":
            play_again_addresses.append(addresses[j])
            play_again_names.append(fila_espera[j])
        elif message.decode() == "play_again_negative":
            send_msg("terminate", addresses[j])
        j += 1


if __name__ == '__main__':
    UDPServerSocket.bind((localIP, localPort))
    while True:
        main()

        send_all("Esperando decisão de rematch de todos jogadores...\n",addresses)
        play_again()
        if len(play_again_addresses) == 0:
            break
