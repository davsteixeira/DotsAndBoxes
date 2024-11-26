import socket
import os
import signal

SERVER_HOST = "localhost"
SERVER_PORT = 1111

BUFFER_SIZE = 1024

global _play_again

def menu(nick):
    print("--------Menu--------")
    print("1. Jogar")
    print("2. Scoreboard Geral")
    print("9. Sair")
    option = input("Digite o número da opção que deseja: ")
    match option:
        case "1":
            msg = "1:" + nick
            skt.sendto(msg.encode(), (SERVER_HOST, SERVER_PORT))
        case "2":
            msg = "2:send_scoreboard"
            skt.sendto(msg.encode(), (SERVER_HOST, SERVER_PORT))

            message = []
            print("\n-----------Scoreboard-----------")
            print("Legenda -→ Nickname : Pontuação", end="\n ")
            while message != b"scoreboard_end":
                bytesAdressPair = skt.recvfrom(BUFFER_SIZE)
                message = bytesAdressPair[0]
                d_message = message.decode()
                if d_message != "scoreboard_end":
                    print(d_message, end =" ")
            print("")

            menu(nick)
        case "9":
            print("Fechando...")
            os.kill(os.getpid(), signal.SIGINT)
        case _:
            print("Opção Inválida, tente novamente")
            menu(nick)

def main():
    global _play_again
    _play_again = ""

    while True:
        try:
            bytesAdressPair = skt.recvfrom(BUFFER_SIZE)
            message = bytesAdressPair[0]
            address = bytesAdressPair[1]

            decodedmsg = message.decode()

            match decodedmsg:
                case "pa":
                    play1 = input("Ponto de origem (Linha / Coluna):")
                    skt.sendto(str.encode(play1), address)
                case "pb":
                    play2 = input("Ponto de destino (Linha / Coluna):")
                    skt.sendto(str.encode(play2), address)

                case "play_again":
                    while _play_again != "y" and _play_again != "n":
                        play_again = input("Gostaria de jogar novamente? <S/N>\n")
                        if play_again == "S" or play_again == "s":
                            skt.sendto(str.encode("play_again_positive"), address)
                            _play_again = "y"
                        elif play_again == "N" or play_again == "n":
                            skt.sendto(str.encode("play_again_negative"), address)
                            _play_again = "n"
                        else:
                            print("Opção Inválida, tente novamente")
                    break
                case "terminate":
                    print("Game ended...")
                    break
                case "menu":
                    menu(nick)
                case _:
                    print(decodedmsg, end="")
        except ConnectionResetError:
            print("Connection Ended")

if __name__ == "__main__":

    skt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    nick = input("Digite seu nickname:")
    menu(nick)

    while True:
        main()
        if _play_again == "y":
            continue
        else:
            break
