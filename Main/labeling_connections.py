__author__ = 'root'
#Tomamos un dataset con etiquetas por cada flow y debemos inicialmente unificar todas estas etiquetas por el mismo ip inicio, ip destino y puerto.
#Para ello usamos un hastable para identificar los mismos id de conexion. Despues sumamos 1 o -1(normal o botnet) de esta manera podemos saber cual es el patron que mas se repite.

import os
import sys
import file_manager as fm


def join_label_form_ips_and_port(path):
    lines = fm.readAllLine(path)#, 'result')
    fileName = 'capture20110819.binetflow-result.labels'
    fileResult = open(path + os.sep + fileName, 'w')
    id_connection_hash = {}
    id_connection_labels_hash = {}
    count = 0
    count2 = 0

    for line in lines:
        count += 1
        text = line.split(' ')
        id_connection = text[0] + '-' + text[1] + '-' + text[2]
        num_label = find_label(text[3]) #1 si es normal y -1 si es botnet, de esta manera para un mismo id_connection en el hash quedara positivo si la mayoria es normal.
        id_connection_hash[id_connection] = id_connection_hash[id_connection] + num_label if id_connection in id_connection_hash else num_label
        label = fm.clear_text(text[3], 'flow=')
        id_connection_labels_hash[id_connection] = id_connection_labels_hash[id_connection] + label + ' ' if id_connection in id_connection_labels_hash else label + ' '

    for connection in id_connection_hash.keys():
        count2 += 1
        label = find_normal_label(id_connection_labels_hash[connection]) if id_connection_hash[connection] > 0 else find_botnet_label(id_connection_labels_hash[connection])
        fileResult.write(connection + '-' + label + '\n')
        if id_connection_hash[connection] != 1 and id_connection_hash[connection] != -1:
            print connection

    fileResult.close()
    print 'done: '+ str(count) +' '+ str(count2)


#############################################################################################################################################################
#Esta funcion esta para mezclar los dos datasets(el que obtuvimos inicialmente y el que teniamos con el modelo de letras) y obtener las etiquetas finales.
#############################################################################################################################################################

def setting_label(path):
    lines = fm.readAllLine(path)
    fileName = 'botnet-capture-20110819-bot-result.pcap.tsv'
    #path_result = '/media/jorge/0622F24F22F2436B/Phd/Data\ Sets/nuevos\ datasets/ctu-13-models/labelled/'
    fileResult = open(path + os.sep + fileName, 'w')
    id_connection_label_hash = {}
    fileResult.write('ModelId	State	LabelName\n')

    for line in lines:
        text = line.split('From')
        if len(text) > 1:
            id_connection = clean_id_connection(text[0])
            id_connection_label_hash[id_connection] = 'From' + fm.clear_text(text[1], '\n')

    lines2 = fm.readAllLine('/home/jorge/Data/aux/')
    count = 0 #para no tener en cuenta la primera linea
    for line in lines2:
        if count != 0:
            text = line.split('-')
            new_id_connection = text[0] + '-' + text[1] + '-' + text[2]
            current_label = id_connection_label_hash[new_id_connection] if new_id_connection in id_connection_label_hash else 'Non-Label'
            text = line.split('\t')
            new_line = text[0] + '-' + current_label + ' ' + text[1] + '\n'
            fileResult.write(new_line)
        count += 1

    fileResult.close()
    print 'done'

def find_label(text):
    #1 si la conexion es normal, -1 si es botnet
    result = 1 if text.find('Normal') != -1 else -1
    return result

def is_normal(label):
    return True if label.find('Normal') != -1 else False

def find_normal_label(text):
    labels = text.split(' ')
    result = 'Normal'
    for label in labels:
        if label.find('Normal') != -1:
            return label

def find_botnet_label(text):
    labels = text.split(' ')
    result = 'Botnet'
    for label in labels:
        if label.find('Botnet') != -1:
            return label

def clean_id_connection(text):
    aux = text.split('-')
    return aux[0] + '-' + aux[1] + '-' + aux[2]

if __name__ == "__main__":
    path = '/home/jorge/Data/capture/'
    #join_label_form_ips_and_port(path)
    setting_label(path)
    print 'the end'
    #args = sys.argv[1:]
    #if args[0] != '-d' or len(args) != 3:
    #    print 'Must supply directory name and a length of the words  "-d <dir-path> <pattern>"'
    #else:
    #    #build_json(args[1], args[2])
    #    build_json_with_length_fixed(args[1])
    #    print 'done'

