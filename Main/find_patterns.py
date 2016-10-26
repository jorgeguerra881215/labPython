__author__ = 'root'

import sys
import os
import file_manager as file
import re
import data_json as data_manager

def search_sequence(path,pattern):
    lines = file.readAllLine(path, 'find_result_to')
    fileName = 'find_result_to_'+pattern
    fileResult = open(path+os.sep+fileName, 'w')
    fileResult.write('Result('+pattern+')'+'|'+' Label '+'|'+' Model ID '+'|'+' State\n')
    count = 0
    for line in lines:
        if count != 0 and len(line) > 1:
            text = line.split('|')[3]
            result = knp(text,pattern)
            if len(result) > 0:
                text = re.sub("\n", "", text)
                dictToken = tokenization(text)
                line = re.sub("\n", "", line)
                line += "  |>>>>"
                for token in dictToken.keys():
                    line += '|'+token+'('+str(dictToken[token])+')'
                newLine = '('+str(len(result))+')|'+line+'\n'
                fileResult.write(newLine)
        count += 1

def ranking_similar_words(path):
    lines = file.readAllLine(path, 'ranking')
    fileName = 'ranking'
    #fileResult = open(path+os.sep+fileName, 'w')
    list_all_words = list()
    ranking = dict()
    count = 0
    for line in lines:
        if count != 0 and len(line) > 1:
            status = file.clear_text(line.split('|')[3])
            if len(status) > 4:
                list_all_words += data_manager.all_word_list(status, 5)

    ranking = build_word_ranking(list_all_words)
    for kword in ranking.keys():
        result_line = kword + ' -> ' + str(ranking[kword]) + '\n'
        print result_line
        #fileResult.write(result_line)

    #fileResult.close()

def build_word_ranking(list_words):
    result = dict()
    list_words.sort()
    for idx, word in enumerate(list_words):
        print word
        for i in range(idx, len(list_words)-1):
            if i < len(list_words) and string_matching(word, list_words[i+1]):
                result[word] = result[word] + 1 if word in result else 1
            else:
                break
    return result


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

def knp(text, pattern):
    # allow indexing into pattern and protect against change during yield
    pattern = list(pattern)
    result = list()
    # build table of shift amounts
    shifts = [1] * (len(pattern) + 1)
    shift = 1
    for pos in range(len(pattern)):
        while shift <= pos and pattern[pos] != pattern[pos-shift]:
            shift += shifts[pos-shift]
        shifts[pos+1] = shift

    # do the actual search
    startPos = 0
    matchLen = 0
    for c in text:
        while matchLen == len(pattern) or \
              matchLen >= 0 and pattern[matchLen] != c:
            startPos += shifts[matchLen]
            matchLen -= shifts[matchLen]
        matchLen += 1
        if matchLen == len(pattern):
            result.append(startPos)
    return result

def tokenization(text):
    text = re.sub(" +", "", text)
    tokens = dict()
    for letter in text:
        tokens[letter] = tokens[letter]+1 if letter in tokens else 1
    return tokens

def build_vectors(path,length):
    fileName = 'state_vectors'
    fileResult = open(path+os.sep+fileName, 'w')
    fileResult.write('State'+'|'+' Vectors'+str(length)+'\n')
    count = 0

if __name__ == "__main__":
    #args = sys.argv[1:]
    #if args[0] != '-d' or len(args) != 2:
    #    print 'Must supply directory name and a pattern to find in "-d <dir-path> <pattern>"'
    #else:
    #    ranking_similar_words(args[1])
    #    print 'done ranking'
    ranking_similar_words('/home/jorge/Data/urank_data')
    print 'game over'