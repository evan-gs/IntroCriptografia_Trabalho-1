import aux_functions as af
import copy
import numpy as np

def keyExpansion(key):
    # Inicia lista de palavras
    w = []

    # Primeiras 4 palavras são cada linha da chave inicial
    for i in range(0,4):
        w.append(key[i])
    
    # Aplica geração de palavras e adiciona na lista
    for i in range(4, 44):
        temp = copy.deepcopy(w[i-1])
        if (i % 4 == 0):
            temp = af.xorRcon(af.subWord(af.rotWord(temp)), af.RCON[(i//4)-1])   
        
        w.append(af.xor(w[i-4], temp))
    
    return w


def addRoundKey(state, roundKey):
    # Aplica XOR entre as matrizes estado e chave de rodada
    roundKey = af.xorMatrix(state, roundKey)
    return roundKey

def subBytes(matrix):
    matrix = np.array(matrix, dtype=np.uint8)
    #Extrai os bits mais e menos significativos
    mais_sig = (matrix >> 4) & 0x0F
    menos_sig = matrix & 0x0F
    
    #Substitui com os valores presentes na posição indicada
    substituido = np.zeros_like(matrix)  #Inicializa a matriz substituída
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            linha = mais_sig[i, j]
            coluna = menos_sig[i, j]
            substituido[i, j] = af.S_BOX[linha][coluna]
    return substituido



def shiftRows(matrix):
    copiedMatrix = copy.deepcopy(matrix)
    # Faz o deslocamento das linhas
    for i in range(0, 4):
        # Primeira coluna se mantem, enquanto nas demais aplica o descolamento das linhas de acordo com índice da coluna
        for j in range(1, 4):
            newPosition = (j+i) % 4
            matrix[i][j] = copiedMatrix[newPosition][j]
    
    return matrix


def mixColumns(matrix, base):
    stateM = np.array(matrix, dtype=np.uint8)
    baseM = np.array(base, dtype=np.uint8)
    
    final = stateM.copy()

    # aqui são feitas as operações de multiplicação de matriz por Galois e as operações XOR para definição de cada elemento da matriz.
    for c in range(4):  
        for i in range(4):
            final[c][i] = (
                af.galois_multiply(baseM[i][0], stateM[c][0]) ^
                af.galois_multiply(baseM[i][1], stateM[c][1]) ^
                af.galois_multiply(baseM[i][2], stateM[c][2]) ^
                af.galois_multiply(baseM[i][3], stateM[c][3])
            )

    return final.copy()

def aes(msg, key):
    
    # Transforma a mensagem e chave em matrizes 4x4 de inteiros
    msgMatrix = [
        [ord(msg[i * 4 + j]) for j in range(4)]
        for i in range(4)
    ]
    keyMatrix = [
        [ord(key[i * 4 + j]) for j in range(4)]
        for i in range(4)
    ]
    print("Matriz 4x4 da mensagem original:")
    af.printMatrix(msgMatrix)
    print("Matriz 4x4 da chave:")
    af.printMatrix(keyMatrix)

    #msgMatrix = af.hexToMatrix("00112233445566778899aabbccddeeff")
    #keyMatrix = af.hexToMatrix("000102030405060708090a0b0c0d0e0f")

    
    #Expansão da chave em 44 palavras
    expandedKey = keyExpansion(keyMatrix)

    # Inicia estado com a própria mensagem
    state = copy.deepcopy(msgMatrix)

    # Inicia as rodadas
    for round in range(0, 11):

        # Gera chave da rodada com 4 palavras
        roundKey = [expandedKey[round*4], expandedKey[(round*4)+1], expandedKey[(round*4)+2], expandedKey[(round*4)+3]]
        #print("Round Key " +  str(round))
        #af.printMatrix(roundKey)

        # Execução da rodada de acordo com seu índice. Comentários abaixo retiram instruções para testagem do algortimo, que mostram resultados das instruções passo a passo
        if round == 0: # Rodada 0
            state = addRoundKey(state, roundKey)
            #print("addRoundKey " + str(round))
            #af.printMatrix(state)

        elif round >= 1 and round <= 9: # Rodada 1 a 9
            state = subBytes(state)
            #print("subBytes " + str(round))
            #af.printMatrix(state)
            state = shiftRows(state)
            #print("shiftRows " + str(round))
            #af.printMatrix(state)
            state = mixColumns(state, af.MIX_C_ENC)
            #print("mixColumns " + str(round))
            #af.printMatrix(state)
            state = addRoundKey(state, roundKey)
            #print("addRoundKey " + str(round))
            #af.printMatrix(state)

        else: # Rodada 10
            state = subBytes(state)
            #print("subBytes " + str(round))
            #af.printMatrix(state)
            state = shiftRows(state)
            #print("shiftRows " + str(round))
            #af.printMatrix(state)
            state = addRoundKey(state, roundKey)
            #print("addRoundKey " + str(round))
            #af.printMatrix(state)

    return state

def main():
    
    #Entrada da mensagem e chave de 128 bits cada
    messageString = input("Insira a mensagem de entrada de 128 bits:\n") #criptografiaetop
    keyString = input("Insira a chave de 128 bits:\n") #qwertyuioplkjhgf

    #Checa tamanho
    if len(messageString) != 16 or len(keyString) != 16:
        print("Mensagem ou chave inserida com tamanho incorreto!")
    else:
        # Executa o algoritmo e imprime resultado em formato de Matrix 4x4 e string
        encryptedMessage = aes(messageString, keyString)
        print("Matriz 4x4 da mensagem criptografada:")
        af.printMatrix(encryptedMessage)
        print("Valores em formato de string:")
        af.printMatrixString(encryptedMessage)




if __name__ == "__main__":
    main()