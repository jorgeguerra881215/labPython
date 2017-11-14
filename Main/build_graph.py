# Script para construir un grafo con las conexiones de un dataset.
__author__ = 'root'
import os
import file_manager as fm

_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9',
            '.', ',', '+', '*', '0']

def list_of_characters():
    count_of_characters = 50
    matrix_result = {}
    for i in _list:
        matrix_result[i] = [0 for j in range(0, count_of_characters)]
    return matrix_result


def build_graph(path):
    lines = fm.readAllLine(path, 'graph_result')
    fileName = 'graph_result.txt'
    fileResult = open(path + os.sep + fileName, 'w')
    fileResult.write('a,b,c,d,e,f,g,h,i,A,B,C,D,E,F,G,H,I,r,s,t,u,v,w,x,y,z,R,S,T,U,V,W,X,Y,Z,1,2,3,4,5,6,7,8,9,.,-,+,*,0' + '\n')
    count = 0 #variable para no usar la primera linea de los data set
    count_selected_element = 0
    matrix = list_of_characters()
    for line in lines:
        if count != 0 and len(line) > 1:
            text = line.split(' ')
            label = text[6]
            character_sequence = fm.clear_text(text[7])
            fill_matrix(label, character_sequence, matrix)
        count += 1

    for key in matrix.keys():
        fileResult.write(str(key) + ', ')
        for i in range(0, len(matrix[key])):
            fileResult.write(str(matrix[key][i]) + ', ')
        fileResult.write('\n')

    return 0

def fill_matrix(label, character_sequence, matrix):
    for i in range(0, len(character_sequence)-1):
        current_character = character_sequence[i]
        next_character = character_sequence[i + 1]
        index_next_character = _list.index(next_character)
        if label == 'Normal':
            matrix[current_character][index_next_character] += 1
        else:
            matrix[current_character][index_next_character] += -1

if __name__ == "__main__":
    build_graph('/home/jorge/Data/build_graph/')
    print 'build graph finished'