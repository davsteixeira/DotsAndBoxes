"""Cria as linhas do jogo com base no tamanho do tabuleiro."""
def criar_tabuleiro(linhas, colunas):
    horizontais = {f"{chr(97 + i)}x{j + 1}": False for i in range(linhas + 1) for j in range(colunas)}
    verticais = {f"{chr(97 + i)}y{j + 1}": False for i in range(linhas) for j in range(colunas + 1)}
    return {**horizontais, **verticais}

"""Exibe o tabuleiro no console."""
def exibir_tabuleiro(linhas, colunas, tabuleiro):
    for i in range(linhas + 1):
        # Linhas horizontais
        linha_h = ""
        for j in range(colunas):
            linha_h += ".---" if tabuleiro[f"{chr(97 + i)}x{j + 1}"] else ".   "
        linha_h += "."
        print(linha_h)

        if i < linhas:
            # Linhas verticais
            linha_v = ""
            for j in range(colunas + 1):
                linha_v += "|   " if tabuleiro[f"{chr(97 + i)}y{j + 1}"] else "    "
            print(linha_v)

"""Verifica se há quadrados formados e atualiza os pontos."""
def verificar_quadrados(tabuleiro, linhas, colunas, pontos):
    for i in range(linhas):
        for j in range(colunas):
            # Nome das linhas que formam o quadrado
            cima = f"{chr(97 + i)}x{j + 1}"
            baixo = f"{chr(97 + i + 1)}x{j + 1}"
            esquerda = f"{chr(97 + i)}y{j + 1}"
            direita = f"{chr(97 + i)}y{j + 2}"

            if tabuleiro[cima] and tabuleiro[baixo] and tabuleiro[esquerda] and tabuleiro[direita]:
                quadrado = f"{chr(97 + i)}{j + 1}"
                if quadrado not in pontos:
                    return quadrado
    return None

"""Função principal para jogar."""
def jogar():
    linhas, colunas = 5, 4  # Tabuleiro 5x4
    tabuleiro = criar_tabuleiro(linhas, colunas)
    pontos = {}
    jogadores = ["Player 1", "Player 2"]
    turno = 0

    while not all(tabuleiro.values()):
        exibir_tabuleiro(linhas, colunas, tabuleiro)
        print(f"\n{jogadores[turno % 2]}, escolha uma linha (ex: ax1):")
        escolha = input().strip()

        if escolha in tabuleiro and not tabuleiro[escolha]:
            tabuleiro[escolha] = True
            quadrado = verificar_quadrados(tabuleiro, linhas, colunas, pontos)
            if quadrado:
                pontos[jogadores[turno % 2]] = pontos.get(jogadores[turno % 2], 0) + 1
                print(f"{jogadores[turno % 2]} formou o quadrado {quadrado}!")
            else:
                turno += 1
        else:
            print("Linha inválida ou já marcada. Tente novamente.")

    exibir_tabuleiro(linhas, colunas, tabuleiro)
    print("\nFim do jogo!")
    for jogador, pontuacao in pontos.items():
        print(f"{jogador}: {pontuacao} ponto(s).")


if __name__ == "__main__":
    jogar()
