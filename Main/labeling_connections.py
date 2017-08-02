__author__ = 'root'
#Tomamos un dataset con etiquetas por cada flow y debemos inicialmente unificar todas estas etiquetas por el mismo ip inicio, ip destino y puerto.
#Para ello usamos un hastable para identificar los mismos id de conexion. Despues sumamos 1 o -1(normal o botnet) de esta manera podemos saber cual es el patron que mas se repite.

import os
import sys
from os.path import basename
import file_manager as fm

_list_file_names = ['','','','','','','','','','','','','','','']
_list_file_names = ['','','','','','','','','','','','','','','']

def repeat_model_id():
    return 0

def join_label_form_ips_and_port(path):
    lines = fm.readAllLine(path)#, 'result')
    fileName = 'capture20110817.binetflow-result.labels'
    fileResult = open(path + os.sep + fileName, 'w')
    id_connection_hash = {}
    id_connection_labels_hash = {}
    count = 0
    count2 = 0

    for line in lines:
        count += 1
        text = line.split(',')
        id_connection = text[1] + ',' + text[2] + ',' + text[3] + ',' + text[0]
        num_label = find_label(text[4]) #1 si es normal y -1 si es botnet, de esta manera para un mismo id_connection en el hash quedara positivo si la mayoria es normal.
        id_connection_hash[id_connection] = id_connection_hash[id_connection] + num_label if id_connection in id_connection_hash else num_label
        label = fm.clear_text(text[4], 'flow=')
        id_connection_labels_hash[id_connection] = id_connection_labels_hash[id_connection] + label + ' ' if id_connection in id_connection_labels_hash else label + ' '

    for connection in id_connection_hash.keys():
        count2 += 1
        label = find_normal_label(id_connection_labels_hash[connection]) if id_connection_hash[connection] > 0 else find_botnet_label(id_connection_labels_hash[connection])
        fileResult.write(connection + ',' + label + '\n')
        if id_connection_hash[connection] != 1 and id_connection_hash[connection] != -1:
            print connection

    fileResult.close()
    print 'done: '+ str(count) +' '+ str(count2)


#############################################################################################################################################################
#Esta funcion esta para mezclar los dos datasets(el que obtuvimos inicialmente y el que teniamos con el modelo de letras) y obtener las etiquetas finales.
#############################################################################################################################################################

def setting_label(lines, lines2, result_name=''):
    #lines = fm.readAllLine(path)
    fileName = 'result-' + result_name + '.pcap.tsv'
    path_result = '/home/jorge/Data/result/' #'/media/jorge/0622F24F22F2436B/Phd/Data\ Sets/nuevos\ datasets/ctu-13-models/labelled/'
    fileResult = open(path_result + os.sep + fileName, 'w')
    id_connection_label_hash = {}
    fileResult.write('ModelId\tLabelName\tLabel\tState\n')
    count = 0
    for line in lines:
        text = line.split(',')
        if count != 0 and len(text) > 14 and text[14].find('Background') == -1:
            proto = text[2]
            ip_o = text[3]
            ip_d = text[6]
            port = text[7]
            label = text[14]
            id_connection = ip_o + '-' + ip_d + '-' + port + '-' + proto #clean_id_connection(text[0])
            id_connection_label_hash[id_connection] = fm.clear_text(label, '\n')
        if len(text) != 15:
            print count
        count += 1

    #lines2 = fm.readAllLine('/home/jorge/Data/aux/')
    count = 0 #para no tener en cuenta la primera linea
    for line in lines2:
        text = line.split('\t')
        if count != 0 and len(text) >= 3:
            #text = line.split('-')
            new_id_connection = text[0] #+ '-' + text[1] + '-' + text[2] + '-' + text[3]
            if new_id_connection in id_connection_label_hash:
                current_label = id_connection_label_hash[new_id_connection]
                informal_label = get_informal_label(current_label)
                #text = line.split('\t')
                new_line = new_id_connection + '\t' + current_label + '\t' + informal_label + '\t' + text[1] + '\n'
                fileResult.write(new_line)
                #if not current_label.find('Background'):
                #    fileResult.write(new_line)
        count += 1

    fileResult.close()
    print 'finish file ' + result_name + ' label: ' + str(len(id_connection_label_hash.keys()))

def get_line_files(path1, path2):
    files = fm.getFiles(path1)
    for file in files:
        file_name = basename(file)
        file_id = file_name.split('.')[0]
        pcap_name = file_id + '.truncated.pcap.tsv'
        #file2 = fm.getFileByName(path2, pcap_name)
        lines1 = fm.readAllLinesByFile(path1, file_name)
        lines2 = fm.readAllLinesByFile(path2, pcap_name)

        setting_label(lines1, lines2, file_id)
    print 'game over'

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

def get_informal_label(label):
    if label.find('Non-Label') != -1:
        return 'Non-Label'
    elif label.find('Botnet') != -1:
        return 'Botnet'
    else:
        return 'Normal'



if __name__ == "__main__":
    path = '/home/jorge/Data/capture/'
    path2 = '/home/jorge/Data/aux/'
    #join_label_form_ips_and_port(path)
    #setting_label(path)
    get_line_files(path, path2)
    print 'the end'
    #args = sys.argv[1:]
    #if args[0] != '-d' or len(args) != 3:
    #    print 'Must supply directory name and a length of the words  "-d <dir-path> <pattern>"'
    #else:
    #    #build_json(args[1], args[2])
    #    build_json_with_length_fixed(args[1])
    #    print 'done'

