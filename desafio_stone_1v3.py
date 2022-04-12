from time import sleep
import random

PAREDE = '▪'
CAMINHO_LIVRE = ' '
CAMINHO_PERCORRIDO = '◦'
ROBO = "☃"
SAIDA = "♣"

ESQUERDA = [0, -1]
DIREITA  = [0, 1]
CIMA     = [-1, 0]
BAIXO    = [1, 0]
DIRECOES = [DIREITA, BAIXO, ESQUERDA, CIMA]

LABIRINTO = [
    ['▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪'], 
    ['▪', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', '▪'], 
    ['▪', ' ', '▪', '▪', '▪', '▪', '▪', '▪', ' ', '▪', '▪', '▪', '▪', '▪', ' ', '▪', ' ', '▪', '▪', '▪'], 
    ['▪', '▪', '▪', '▪', '▪', '▪', ' ', ' ', ' ', ' ', ' ', ' ', '▪', '▪', '▪', '▪', ' ', ' ', ' ', '▪'], 
    ['▪', ' ', ' ', ' ', ' ', ' ', ' ', '▪', ' ', '▪', '▪', ' ', ' ', ' ', ' ', '▪', '▪', '▪', ' ', '▪'], 
    ['▪', '▪', '▪', '▪', '▪', ' ', '▪', '▪', ' ', ' ', '▪', '▪', ' ', '▪', ' ', ' ', ' ', '▪', ' ', '▪'], 
    ['▪', '▪', ' ', ' ', ' ', ' ', '▪', '▪', ' ', '▪', '▪', ' ', ' ', '▪', '▪', ' ', '▪', '▪', ' ', '▪'], 
    ['▪', ' ', ' ', '▪', ' ', '▪', '▪', '▪', ' ', '▪', '▪', ' ', '▪', '▪', ' ', ' ', '▪', '▪', ' ', '▪'], 
    ['▪', '▪', ' ', '▪', ' ', '▪', ' ', ' ', ' ', ' ', '▪', ' ', ' ', '▪', ' ', '▪', '▪', ' ', ' ', '▪'], 
    ['▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '▪', '♣', '▪']
]

posicao_inicial_x = int(input('insira a posicao x:'))
posicao_inicial_y = int(input('insira a posicao y:'))

posicao_inicial = []
posicao_inicial.append(posicao_inicial_x); posicao_inicial.append(posicao_inicial_y)

while LABIRINTO[posicao_inicial[0]][posicao_inicial[1]] == PAREDE:

    print('\nposição invalida, por favor coloque outra:\n')

    posicao_inicial_x = int(input('insira a posicao x:'))
    posicao_inicial_y = int(input('insira a posicao y:'))

    posicao_inicial = (posicao_inicial_x, posicao_inicial_y)

PILHA = [tuple(posicao_inicial)]

def busca_indice (lista, valor):
    '''Essa função busca o índice da saída do labirinto dentro da lista de listas do mesmo

    input:
        lista(lista): A lista de listas onde a palavra será procurada,
        valor: palavra a ser procurada (pode ser uma string, lista, ou qualquer tipo de dado)
        
    Returns:
        indice(lista): Retorna uma lista com os indices da palavra dentro da lista de listas
    '''

    for x in lista:
        if valor in x:
            indice = [lista.index(x), x.index(valor)]
    return indice

INDICE_SAIDA = busca_indice(LABIRINTO, SAIDA)

def print_labirinto():
    print("")
    for linha in LABIRINTO:
        print("".join(linha))
    print("")

print_labirinto()
sleep(0.5)


def movimento(posicao: tuple, direcao: list):
    '''Essa função movimenta o robo na direção dada
    
    Args:
    posição(tupla): Posição atual, direção(lista): Direção dada
    
    Returns:
    posicao_andada(tupla): Retorna a posição do robo após andar
    '''
        
    posicao_andada = [list(posicao)[0] + direcao[0], list(posicao)[1] + direcao[1]]

    LABIRINTO[list(posicao)[0]][list(posicao)[1]] = CAMINHO_PERCORRIDO

    PILHA.append(tuple(posicao_andada))

    LABIRINTO[posicao_andada[0]][posicao_andada[1]] = ROBO

    return(posicao_andada)

def voltar(posicao: tuple, direcao: list, contador: int) -> tuple:
    '''Essa função faz o robo voltar para a última casa andada antes de ser encurralado
    e testar as 4 direções sem um caminho viável

    Args: 
        posição(tupla): Posição atual, direção(lista): Direção testada,
        contador(inteiro): Quantidade de direções testadas
    
    Returns:
        posicao_andada(tupla): Retorna a posição que o robo voltou
    '''
    
    if contador == 4 and verifica_movimento(posicao, direcao) == False:
            
            PILHA.pop()

            passo_anterior = PILHA[-1]
            
            posicao_andada = [passo_anterior[0], passo_anterior[1]]

            LABIRINTO[list(posicao)[0]][list(posicao)[1]] = CAMINHO_PERCORRIDO

            LABIRINTO[posicao_andada[0]][posicao_andada[1]] = ROBO

            print_labirinto()
            sleep(0.5)

            return(posicao_andada)
    

def verifica_movimento(posicao: tuple, direcao: list) -> bool:
    '''Essa função verifica se o robo pode andar na direção dada
    
    Args:
    posição(tupla): Posição atual, direção(lista): direção dada
    
    Returns:
    bool: True se a posição pretendida for viável, e False caso contrário
    '''

    posicao_pretendida = [list(posicao)[0] + direcao[0], list(posicao)[1] + direcao[1]]

    if (
        LABIRINTO[posicao_pretendida[0]][posicao_pretendida[1]] == PAREDE
        or LABIRINTO[posicao_pretendida[0]][posicao_pretendida[1]] == CAMINHO_PERCORRIDO
        ):
        return False

    elif (
        LABIRINTO[posicao_pretendida[0]][posicao_pretendida[1]] == CAMINHO_LIVRE
        or LABIRINTO[posicao_pretendida[0]][posicao_pretendida[1]] == SAIDA
        ):
        return True

def main(x, y):

    POSICAO_INICIAL = (x, y)

    LABIRINTO[POSICAO_INICIAL[0]][POSICAO_INICIAL[1]] = ROBO

    print_labirinto()
    sleep(0.5)

    POSICAO_ATUAL = POSICAO_INICIAL

    qntd_direcoes_testadas = 0

    POSICAO_RETORNADA = []

    DIRECOES = [DIREITA, BAIXO, ESQUERDA, CIMA]
    
    while POSICAO_ATUAL != INDICE_SAIDA:

        if DIRECOES != []:
            posicao_inicio_turno = POSICAO_ATUAL
        else:
            posicao_inicio_turno = POSICAO_RETORNADA
            POSICAO_ATUAL = POSICAO_RETORNADA

        DIRECOES = [DIREITA, BAIXO, ESQUERDA, CIMA]

        while POSICAO_ATUAL == posicao_inicio_turno and qntd_direcoes_testadas != 4:
            
            direcao_testada = random.choice(DIRECOES)

            if verifica_movimento(POSICAO_ATUAL, direcao_testada):

                indice_direcao = DIRECOES.index(direcao_testada)

                POSICAO_ATUAL = movimento(POSICAO_ATUAL, direcao_testada)

                print_labirinto()
                sleep(0.5)
            
            else: #Conta quantas direções já foram testadas, e apaga a direção testada de DIREÇÔES

                indice_direcao = DIRECOES.index(direcao_testada)

                DIRECOES.pop(indice_direcao)

                qntd_direcoes_testadas += 1

                POSICAO_RETORNADA = voltar(POSICAO_ATUAL, direcao_testada, qntd_direcoes_testadas)

        qntd_direcoes_testadas = 0
        
    print('\nO jogo terminou, esse é o caminho correto!')

    for i in range(len(PILHA)): 
        #pega os valores da PILHA e substitui no LABIRINTO por um certo, para mostrar o caminho da saída
        LABIRINTO[PILHA[i][0]][PILHA[i][1]] = '✔'
    print_labirinto()

if __name__ == "__main__":
    main(posicao_inicial[0], posicao_inicial[1])
