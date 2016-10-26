__author__ = 'root'
import os
import file_manager as file
import data_json as data_manager
import math
import sys

def connection_ranking(path, words_vector):
    fileName = 'ranking_connection_similar_to_'+'_'.join(words_vector)+'_.txt'
    fileResult = open(path+os.sep+fileName, 'w')
    fileResult.write('Value(URank) | Note | Label | Model Id |\n')

    value_document_vector = dict()
    document_vector = document_vectors(path, len(words_vector[0]),value_document_vector)
    aux_dict = dict()
    w_ranking = dict()
    for k in document_vector.keys():
        build_word_ranking(w_ranking, document_vector[k], k, aux_dict)

    #result_dict = uRank(words_vector, document_vector, w_ranking)
    result_dict = similar(words_vector, document_vector, w_ranking)
    d_view = [(v,k) for k,v in result_dict.iteritems()]
    d_view.sort(reverse=True)
    for v, k in d_view:
        if v != 0.0:
            fileResult.write(str(v)+' | '+value_document_vector[k])
        print '%s => %s' % (k, v)
    fileResult.close()

#////////////// Similarity Computation ////////////////////////////
def similar(word_vector, document_vector, word_ranking):
    result = dict()
    for word in word_vector:
        for doc in word_ranking[word][1]:
            result[doc] = float(word_ranking[word][1][doc] + result[doc]) if doc in result else float(word_ranking[word][1][doc])

    return result
#////////////// uRank Ranking Computation /////////////////////////
def uRank(word_vector, document_vector, word_ranking):
    result = dict()
    for word in word_vector:
        for k_doc in document_vector:
            N = len(document_vector)
            norm_T = math.sqrt(float(len(word_vector)))
            norm_d = math.sqrt(float(len(document_vector)))
            tf_idf = TF_IDF(word, k_doc, word_ranking, N)
            s1 = float(tf_idf) / (norm_d * norm_T)
            result[k_doc] = result[k_doc] + s1 if k_doc in result else s1
    return result

def TF_IDF(word, k_document, w_ranking, n):
    if k_document in w_ranking[word][1]:
        f = w_ranking[word][1][k_document]
    else:
        return 0
    maxF = 0
    for k in w_ranking.keys():
        if k != word and k_document in w_ranking[k][1]:
            maxF = w_ranking[k][1][k_document] if w_ranking[k][1][k_document] > maxF else maxF

    tf = float(f) / float(maxF)
    idf = math.log10(n / float(len(w_ranking[word][1])))
    return tf*idf


#/////////////// Building Connections Vector ///////////////////
def document_vectors(path,len_of_words,value_document_vector):
    lines = file.readAllLine(path, 'ranking')
    list_all_words = dict()
    count = 0
    for line in lines:
        text = line.split('|')
        if count != 0 and len(text) == 4:
            connection = line.split('|')
            note = file.clear_text(connection[0])
            label = file.clear_text(connection[1])
            model = file.clear_text(connection[2])
            state = file.clear_text(connection[3])
            if len(state) > len_of_words:
                #making word vector for connections
                list_all_words[note] = data_manager.all_word_list(state, len_of_words)
                value_document_vector[note] = note +' | '+ label +' | '+ model + '\n'
        count += 1
    return list_all_words

#//////////////////////// Build Word Ranking //////////////////////
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

######### Making your script come true #########
#if __name__ == "__main__":
#    args = sys.argv[1:]
#    print args[0]
#    print args[1]
#    print args[2]
#    if args[0] != '-d' or len(args) != 3:
#        print 'Must supply directory name and a length of words to build e.g: "-d <dir-path> <number>"'
#    else:
#        word_vector = args[2].split('>>')
#        #connection_ranking(args[1], word_vector)
#    print 'done'