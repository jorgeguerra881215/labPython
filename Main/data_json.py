__author__ = 'jorge'
#Crear el dataset (json) que utiliza RiskID a partir del dataset de Stratosphere.


import os
import sys
import file_manager as fm


def build_json(path, word_len):
    lines = fm.readAllLine(path, 'dataset_Cx')
    fileName = 'dataset_Cx.json'
    fileResult = open(path + os.sep + fileName, 'w')
    fileResult.write('[')
    count = 0 #variable para no usar la primera linea de los data set
    count_selected_element = 0
    for line in lines:
        if count != 0 and len(line) > 1:
            text = line.split('|')
            description_before_clear = fm.clear_text(text[3])
            if len(description_before_clear) > 20:
                id = fm.clear_text(text[0])[1:-1]
                id_value = fm.clear_text(text[2])
                title = fm.clear_text(text[1], "-")
                #making all word
                document = ''
                for word in all_word(description_before_clear, int(word_len)):
                    document += word + ' '
                description = document
                #Ponerle Unlabelled a las conexiones multiplo de 4 en la lista para obtener un cuarto de las conexiones como unlabelled.
                #title = 'Unlabelled' if count_selected_element % 4 == 0 else create_label(title)
                data_json(fileResult, id, title, description, id_value)
                count_selected_element += 1
        count += 1
    fileResult.write(']')
    fileResult.close()

#Crear justamente el json con secuencias de longitud 5, 10 y 15 a partir del dataset 22, 45 o 87
def build_json_with_length_fixed(path):
    lines = fm.readAllLine(path, 'dataset_Cx')
    fileName = 'dataset_Cx.json'
    fileResult = open(path + os.sep + fileName, 'w')
    fileResult.write('[')
    count = 0 #variable para no usar la primera linea de los data set
    count_selected_element = 0
    id_list = []
    clusters = get_clusters()
    for line in lines:
        if count != 0 and len(line) > 1:
            text = line.split('|')
            description_before_clear = fm.clear_text(text[3])
            id = fm.clear_text(text[0])[1:-1]
            if len(description_before_clear) > 20 and id not in id_list:
                #id = fm.clear_text(text[0])[1:-1]
                id_list.append(id)
                id_value = fm.clear_text(text[2])
                title = fm.clear_text(text[1], "-")
                #making all word
                document = ''
                for word in all_word(description_before_clear, 5):
                    document += word + ' '
                for word in all_word(description_before_clear, 10):
                    document += word + ' '
                for word in all_word(description_before_clear, 15):
                    document += word + ' '
                description = document
                title = create_label(title)#'Unlabelled' if count_selected_element % 4 == 0 else create_label(title)
                data_json(fileResult, id, title, description, id_value, clusters[count_selected_element])
                count_selected_element += 1
        count += 1
    fileResult.write(']')
    fileResult.close()

#Crear justamente el json con secuencias de longitud 5, 10 y 15 a partir del dataset c13-full
def build_json_with_length_fixed_using_c13_full(path):
    lines = fm.readAllLine(path, 'dataset_Cx')
    fileName = 'dataset_Cx.json'
    fileResult = open(path + os.sep + fileName, 'w')
    fileResult.write('[')
    count = 0 #variable para no usar la primera linea de los data set
    count_selected_element = 0
    id_list = []
    clusters = get_clusters()
    for line in lines:
        if count != 0 and len(line) > 1:
            text = line.split(' ')
            description_before_clear = fm.clear_text(text[7])
            id = fm.clear_text(text[0])#[1:-1]
            if len(description_before_clear) > 20 and id not in id_list:
                #id = fm.clear_text(text[0])[1:-1]
                id_list.append(id)
                #id_connection = text[1] + '-' + text[2] + '-' + text[3] + '-' + text[4]
                id_value = text[1] + '-' + text[2] + '-' + text[3] + '-' + text[4] #fm.clear_text(text[2])
                title = text[6]#fm.clear_text(text[1], "-")
                #making all word
                document = ''
                for word in all_word(description_before_clear, 5):
                    document += word + ' '
                for word in all_word(description_before_clear, 10):
                    document += word + ' '
                for word in all_word(description_before_clear, 15):
                    document += word + ' '
                description = document
                title = create_label(title)#'Unlabelled' if count_selected_element % 4 == 0 else create_label(title)
                data_json(fileResult, id, title, description, id_value, clusters[count_selected_element])
                count_selected_element += 1
        count += 1
    fileResult.write(']')
    fileResult.close()

def all_word(text, length):
    if len(text) < length:
        yield text
    for idx in xrange(0, len(text) - length + 1):
        yield text[idx:length + idx]


def all_word_list(text, length):
    result = list()
    if len(text) < length:
        result.append(text)
        return result
    for idx in xrange(0, len(text) - length + 1):
        result.append(text[idx:length + idx])
    return result

def get_clusters():
    result = []
    dir = "/home/jorge/Data/cluster"
    lines = fm.readAllLine(dir)
    for line in lines:
        cluster = line[len(line) - 2:len(line) - 1]
        result.append(cluster)
    return result


def create_label(text):
    text = 'Normal' if text.find('Normal') != -1 else 'Botnet'
    return text


def data_json(file, id, title, description, id_value, cluster):
    file.write('{')
    file.write('"id":' + '"' + id + '",\n')
    file.write('"title":' + '"' + title + '",\n')
    file.write('"uri": "http://www.mendeley.com/catalog/robotics-motor-learning-neurologic-recovery/",\n')
    file.write('"eexcessURI": "http://www.mendeley.com/catalog/robotics-motor-learning-neurologic-recovery/",\n')
    file.write('"creator": "David J Reinkensmeyer, Jeremy L Emken, Steven C Cramer",\n')
    file.write('"description":' + '"' + description + '",\n')
    file.write('"collectionName": "",\n')
    file.write('"keyword":"",\n')
    file.write('"observation":"",\n')
    file.write('"connection_id":' + '"' + id_value + '",\n')
    file.write('"cluster":' + '"' + cluster + '",\n')
    file.write('"facets": {"provider": "mendeley","year": "2004"}\n')
    file.write('},')


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] != '-d' or len(args) != 3:
        print 'Must supply directory name and a length of the words  "-d <dir-path> <pattern>"'
    else:
        #build_json(args[1], args[2])
        build_json_with_length_fixed(args[1])
        print 'done'

