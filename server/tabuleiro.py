from terminal import T_BBLUE, T_FBLACK, T_RESET, T_BGREEN


class Tabuleiro:

    _x: int
    _y: int
    _player: int
    _player1_points: int
    _player2_points: int
    _player1_address: tuple
    _player2_address: tuple
    _both_players_address : list
    _send_address: tuple
    _total_squares: int
    _point_per_square : int
    _moves : int
    _con: list[list[str]]

    def __init__(self, x: int, y: int):
        self._player = 1
        self._player1_points = 0
        self._player2_points = 0
        self._total_squares = 0
        self._point_per_square = 10
        self._x = x
        self._y = y
        self._moves = 0
        self._con = [
            ['x' for i in range(x*y)] 
                for j in range(x*y)]

    def active_address(self):
        self._both_players_address = [self._player1_address, self._player2_address]
        if self._player == 1:
            self._send_address = self._player1_address
        else:
            self._send_address = self._player2_address

    def addresses_management(self, address1: tuple, address2: tuple):
        from server import send_msg

        self._player1_address = address1
        send_msg("Você é o Jogador 1 : P1\n", self._player1_address)
        self._player2_address = address2
        send_msg("Você é o Jogador 2 : P2\n", self._player2_address)
        
    def get_num(self, x, y):
        return x + (self._x * y)

    def connect(self, x, y, z ,w):
        pa = self.get_num(x, y)
        pb = self.get_num(z, w)
        #print(pa, pb)
        self._con[pa][pb] = "O"
        self._con[pb][pa] = "O"


    def read_play(self):
        from server import receive_msg

        pa = receive_msg("pa", self._send_address)
        pb = receive_msg("pb",self._send_address)

        av = pa.split(" ")
        ax, ay = int(av[0]), int(av[1])

        bv = pb.split(" ")
        bx, by = int(bv[0]), int(bv[1])

        return (ax, ay), (bx, by)

    def validate_play(self, pta: tuple, ptb: tuple):
        from server import send_msg
        from server import send_all

        pta1 = self.get_num(int(pta[0]), int(pta[1]))
        ptb1 = self.get_num(int(ptb[0]), int(ptb[1]))

        # validar jogada
        if pta[0] is not ptb[0] and pta[1] is not ptb[1]:
            send_msg("Jogada Inválida, tente novamente\n", self._send_address)
            return "invalid_play"
        elif pta[0] >= self._x or ptb[0] >= self._x:
            send_msg("Jogada Inválida, fora dos limites do tabuleiro, tente novamente\n", self._send_address)
            return "invalid_play"
        elif pta[1] >= self._y or ptb[1] >= self._y:
            send_msg("Jogada Inválida, fora dos limites do tabuleiro, tente novamente\n", self._send_address)
            return "invalid_play"
        elif pta[0] - ptb[0] > 1 or pta[1] - ptb[1] > 1:
            send_msg("Jogada Inválida, tente novamente\n", self._send_address)
            return "invalid_play"
        elif ptb[0] - pta[0] > 1 or ptb[1] - pta[1] > 1:
            send_msg("Jogada Inválida, tente novamente\n", self._send_address)
            return "invalid_play"
        elif pta == ptb:
            send_msg("Jogada Inválida, marque dois pontos diferentes para fazer uma linha, tente novamente\n", self._send_address)
            return "invalid_play"
        elif self._con[pta1][ptb1] == "O":
            send_msg("Jogada Inválida, esta jogada já foi feita em outro turno, tente novamente\n", self._send_address)
            return "invalid_play"
        else:
            self.connect(int(pta[0]), int(pta[1]), int(ptb[0]), int(ptb[1]))
            coords = "".join([f"Coordenadas jogadas pelo P{self._player}: ", str(pta), str(ptb), "\n"])
            send_all(coords,self._both_players_address)
            return "valid_play"

    def game(self):
        from server import send_msg
        from server import send_all

        while True:
            self.active_address()

            self.mostra_tabuleiro()
            
            if self._moves == 0:
                    break
            
            try:
                pta, ptb = self.read_play()
            except (ValueError, IndexError):
                send_msg("Erro na jogada, tente novamente com o formato (Linha Coluna) *com espaço*\n",self._send_address)
                continue

            if self.validate_play(pta,ptb) == "invalid_play":
                continue
            else:
                pass

            if self.verifica_quadrados() == "point":
                continue
            else:
                pass

            self.mostra_tabuleiro()

            if self._moves == 0:
                break

            send_msg("Esperando a jogada do outro jogador...\n", self._send_address)

            self._player = 1 if self._player == 2 \
                else 2

        winner : tuple
        winner_name : str
        if self._player1_points > self._player2_points:
            winner = self._player1_address
            send_all("\nJogador 1 ganhou !!!!!!!!\n",self._both_players_address)
        elif self._player2_points > self._player1_points:
            winner = self._player2_address
            send_all("\nJogador 2 ganhou !!!!!!!!\n", self._both_players_address)
        else:
            winner = ("draw","draw")
            send_all("\nEmpatou :(\n", self._both_players_address)
        return winner


    def verifica_quadrados(self):
        from server import send_all

        squares = 0
        for i in range(self._x -1):
            for j in range(self._y -1):
                
                cons = 0

                # esq-cima e dir-cima
                ni = self.get_num(i, j)
                nj = self.get_num(i + 1, j)

                if self._con[ni][nj] == 'O':
                    cons = cons + 1

                # dir-cima e dir-baixo
                ni = self.get_num(i + 1, j)
                nj = self.get_num(i + 1, j + 1)
                
                if self._con[ni][nj] == 'O':
                    cons = cons + 1

                # dir-baixo e esq-baixo
                ni = self.get_num(i + 1, j + 1)
                nj = self.get_num(i, j + 1)
                
                if self._con[ni][nj] == 'O':
                    cons = cons + 1

                # esq-baixo e esq-cima
                ni = self.get_num(i, j + 1)
                nj = self.get_num(i, j)
                
                if self._con[ni][nj] == 'O':
                    cons = cons + 1

                if cons == 4:
                    #print(f"({i}, {j}), ({i+1}, {j}), " +
                    #      f"({i+1}, {j+1}), ({i}, {j+1})")
                    squares = squares + 1

        #Jogador pontua quando há mudança no valor total de quadrados no tabuleiro
        if self._total_squares is not squares:
            diff = squares - self._total_squares
            if self._player == 1:
                self._player1_points = self._player1_points + (diff * self._point_per_square)
                send_all(f"Jogador 1 pontuou e agora está com{self._player1_points : 04d}\n",self._both_players_address)
            else:
                self._player2_points = self._player2_points + (diff * self._point_per_square)
                send_all(f"Jogador 2 pontuou e agora está com{self._player2_points : 04d}\n",self._both_players_address)
            self._total_squares = squares
            return "point"
        else:
            return "pass"


    def mostra_tabuleiro(self):
        from server import send_msg

        counter = 0

        linha = 0

        send_msg((T_BGREEN + "|  DOTS & BOXES  |" + T_RESET),self._send_address)

        while (linha != self._y):

            #########

            send_msg(("\n" + T_BGREEN + "|" + T_RESET),self._send_address)
            for i in range(self._x - 2):

                pa = self.get_num(linha, i)
                pb = self.get_num(linha, i + 1)

                if self._con[pa][pb] == 'O':
                    send_msg((T_BBLUE + T_FBLACK + ".____" + T_RESET),self._send_address)
                else:
                    send_msg((T_BBLUE + T_FBLACK + ".    " + T_RESET),self._send_address)
                    counter += 1

            send_msg((T_BBLUE + T_FBLACK + "." + T_RESET),self._send_address)
            send_msg((T_BGREEN + "|" + T_RESET),self._send_address)

            #########

            send_msg(("\n" + T_BGREEN + "|" + T_RESET),self._send_address)

            for i in range(self._x - 1):

                pa = self.get_num(linha, i)
                pb = self.get_num(linha + 1, i)
                if self._con[pa][pb] == 'O':
                    send_msg((T_BBLUE + T_FBLACK + "|" + T_RESET), self._send_address)
                else:
                    send_msg((T_BBLUE + T_FBLACK + " " + T_RESET), self._send_address)
                    counter += 1

                if i < self._x - 2:
                    send_msg((T_BBLUE + T_FBLACK + "    " + T_RESET), self._send_address)

            send_msg((T_BGREEN + "|" + T_RESET),self._send_address)
            linha += 1

        send_msg(("\n" + T_BGREEN + "|" + T_RESET), self._send_address)
        #send_msg((T_BBLUE + T_FBLACK + ''.join(['.    ' for i in range(self._x - 2)]) + T_RESET), self._send_address)
        for i in range(self._x - 2):
            pa = self.get_num(linha, i)
            pb = self.get_num(linha, i + 1)
            if self._con[pa][pb] == 'O':
                send_msg((T_BBLUE + T_FBLACK + ''.join(['.____']) + T_RESET), self._send_address)
            else:
                send_msg((T_BBLUE + T_FBLACK + ''.join(['.    ']) + T_RESET), self._send_address)
                counter += 1
        send_msg((T_BBLUE + T_FBLACK + "." + T_RESET ), self._send_address)
        send_msg((T_BGREEN + "|" + T_RESET + "\n"), self._send_address)
        if self._player == 1:
            send_msg((T_BGREEN + f"| P1      - {self._player1_points : 04d} |" + T_RESET + "\n"), self._send_address)
        else:
            send_msg((T_BGREEN + f"| P2      - {self._player2_points : 04d} |" + T_RESET + "\n"), self._send_address)
        self._moves = counter
        print(self._moves)

    def __str__(self):
        ss = ""
        for i in range(self._x * self._y):
            for j in range(self._x * self._y):
                ss += " " + self._con[i][j]
            ss += "\n"
        return ss
