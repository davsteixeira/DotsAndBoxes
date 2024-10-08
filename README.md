# DotsAndBoxes

## - Enunciado: Implementar o jogo Dots and Boxes, EM QUINTETOS, com suporte a partidas online. Mais informaçẽs sobre o jogo podem ser obtidas em nos seguinte links:
  https://en.wikipedia.org/wiki/Dots_and_boxes
  https://mathforlove.com/lesson/dots-and-boxes-game/
  
## - Especificação: Deverão ser criadas duas aplicações: um cliente e um servidor. 
  - O cliente deverá conectar no servidor (através do endereço IP e porta), autenticando e posteriormente solicitando ingressar em uma partida. 
  - O servidor deverá colocar o cliente em uma fila de espera. Quando o segundo cliente solicitar a partida, ambos serão adicionados na mesma sessão. 
  - Os clientes jogarão um contra o outros até que o jogo finalize ou um deles abandone a partida. O servidor deverá contabilizar 3 pontos por vitória e armazenar a pontuação em um ranking. Jogadores     que desconectarem da partida antes do final serão penalizados em 1 ponto. 
  - O cliente poderá realizar cadastro e visualizar o ranking através do cliente. 

## - Pontuação: 
  - (2 pontos): O jogo permite que dois jogadores disputem uma partida até o final.
  - (3 pontos): Múltiplas partidas podem ocorrer ao mesmo tempo.
  - (1 ponto): Persistência do ranking (arquivo ou banco de dados) e consulta do ranking através do cliente.
  - (2 ponto): O jogador poderá ingressar novamente na fila após uma partida sem necessitar fechamento do cliente ou servidor
  - (2 ponto): Correta utilização do padrão publish-subscribe e orientação a objetos

## - Pontos extras: 
  - (1 ponto): Suporte a partida entre 3x jogadores (mesma sessão)
  - (1 ponto): Interface gráfica para o cliente (Python; pygame)
  - (1 ponto): Ofuscação/criptografia do protocolo ou "anti-hack"

## - Entregáveis: Código-fonte do cliente e servidor (ambos em Python), descrição do protocolo criado (mensagens) e tutorial de como instalar/executar as aplicações.
