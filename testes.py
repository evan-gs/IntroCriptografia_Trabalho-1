import copy
import aux_functions as af

def shiftRows(matrix):
    for i in range(1,4):
        copiedRow = copy.deepcopy(matrix[i])
        for j in range(0,4):
            newPosition = (j+i) % 4
            matrix[i][j] = copiedRow[newPosition]
        
    return matrix


matrix = [
    [0x63, 0x7c, 0x77, 0x7b],
    [0x01, 0x67, 0x2b, 0xfe],
    [0xca, 0x82, 0xc9, 0x7d],
    [0xd4, 0xa2, 0xaf, 0x9c]
    ]

print(matrix)
print(shiftRows(matrix))
a = 0x11
print(type(a))
print(a == 17)

word = [0x11, 0x10, 0xA5, 0xDE]
print(word)
word = af.xorRcon(word, 2)
for w in word:
    print(hex(w))
#word = af.rotWord(word)
#print(word)
#print(hex(af.S_BOX[3][2]))

# Example hex values

# String de exemplo
hex_string = "00112233445566778899aabbccddeeff"



# Exibir a matriz
af.printMatrix(matrix)



hex_values = "00112233445566778899aabbccddeeff"
bytearray.fromhex("00112233445566778899aabbccddeeff").decode()
print(bytearray)
array = []
for i in range(0, len(hex_values), 2):
    array.append(int(hex_values[i:i+1], 16))
    print(hex(array[i]))

print(array)


