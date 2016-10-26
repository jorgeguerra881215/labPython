__author__ = 'root'
import os
import file_manager as file
import re
import data_json as data_manager
import operator
import connection_ranking as rank


def all_word(text, length):
    if len(text) < length:
        yield text
    for idx in xrange(0, len(text)-length+1):
        yield text[idx:length+idx]

def ranking_similar_words(path,len_of_words):
    lines = file.readAllLine(path, 'ranking')
    fileName = 'ranking'
    #fileResult = open(path+os.sep+fileName, 'w')
    list_all_words = dict()
    result = dict()
    aux_dict = dict()
    count = 0
    for line in lines:
        text = line.split('|')
        if count != 0 and len(text) == 4:
            connection = line.split('|')
            text = connection[3]
            status = file.clear_text(text)
            note = file.clear_text(connection[0])
            if len(status) > len_of_words:
                #making word vector for connections
                list_all_words[note] = data_manager.all_word_list(status, len_of_words)
        count += 1
    for k in list_all_words.keys():
        build_word_ranking(result, list_all_words[k], k,aux_dict)

    # printing result
    d_view = [(v,k) for k,v in aux_dict.iteritems()]
    d_view.sort(reverse=True)
    for v,k in d_view:
        count = result[k][0]
        if count > 1:
            meta_data = ''
            dictMetaData = result[k][1]
            for k2 in dictMetaData.keys():
                meta_data += k2 + '(' + str(dictMetaData[k2])+'),'
            print k + ' |=> ' + str(count) + ' - ' + meta_data

    #for k in result.keys():
    #    count = result[k][0]
    #    if count > 1:
    #        meta_data = ''
    #        dictMetaData = result[k][1]
    #        for k2 in dictMetaData.keys():
    #            meta_data += k2 + '(' + str(dictMetaData[k2])+'),'
    #        print k + ' |=> ' + str(count) + ' - ' + meta_data

    #d_view = [(v,k) for k,v in result.iteritems()]
    #d_view.sort(reverse=True)
    #for v,k in d_view:
    #    print '%s => %s' % (k,v)

    #fileResult.write(result_line)

    #fileResult.close()

def build_word_ranking(dic, list_words, idConnection, aux_dict):
    list_words.sort()
    for w in list_words:
        if w in dic:
            current_value = dic[w]
            current_value[0] += 1
            current_value[1][idConnection] = current_value[1][idConnection] + 1 if idConnection in current_value[1] else 1
            aux_dict[w] += 1
        else:
            dic[w] = [1, {idConnection: 1}]
            aux_dict[w] = 1
    return dic

#def build_word_ranking(list_words):
#    result = dict()
#    list_words.sort()
#    for idx, word in enumerate(list_words):
#        for i in range(idx, len(list_words)-1):
#            if i < len(list_words) and string_matching(word, list_words[i+1]):
#                result[word] = result[word] + 1 if word in result else 1
#            else:
#                break
#    return result


def string_matching(t1, t2):
    if len(t1) != len(t2):
        return False
    if len(t1) == 1:
        return t1 == t2
    t1_sub1 = t1[0:len(t1)/2]
    t1_sub2 = t1[len(t1)/2:len(t1)]
    t2_sub1 = t2[0:len(t2)/2]
    t2_sub2 = t2[len(t2)/2:len(t2)]
    return string_matching(t1_sub1, t2_sub1) and string_matching(t1_sub2, t2_sub2)

def string_sort(lista):
    lista.sort()
    return lista

def test(int,array):

    return False

if __name__ == "__main__":
    w_vector = ['+Y.h.', '*z*0Z', '.z.Z*']
    rank.connection_ranking('/home/jorge/Data/urank_data/ranking', w_vector)
    #ranking_similar_words('/home/jorge/Data/urank_data/ranking', 5)
    print "done"
