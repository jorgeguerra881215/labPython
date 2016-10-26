__author__ = 'jorge'

import os
import sys
import file_manager as fm

def filter_data(path,word_len):
    lines = fm.readAllLine(path, 'dataset_Cx')
    fileName = 'filter_data.txt'
    fileResult = open(path+os.sep+fileName, 'w')
    fileResult.write(' Note | Label | Model Id | State |'+'\n')
    count = 0 #variable para no usar la primera linea de los data set
    count_selected_element = 0
    for line in lines:
        text = line.split('|')
        if count != 0 and len(line) > 1 and len(text) > 3:
            #text = line.split('|')
            description_before_clear = fm.clear_text(text[3])
            if len(description_before_clear) > 20:
                #print line
                id = fm.clear_text(text[0])[1:-1]
                id_value = fm.clear_text(text[2])
                title = fm.clear_text(text[1], "-")
                fileResult.write(id + ' | ' + title + ' | ' + id_value  + '\n')
        count += 1
    fileResult.write('\n')
    fileResult.close()

if __name__ == "__main__":
    args = sys.argv[1:]
    if args[0] != '-d' or len(args) != 3:
        print 'Must supply directory name and a length of the words  "-d <dir-path> <pattern>"'
    else:
        #build_json(args[1], args[2])
        filter_data(args[1], args[2])
        print 'done'
