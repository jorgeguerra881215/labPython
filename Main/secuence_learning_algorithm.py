__author__ = 'root'
import os
import operator
import file_manager as fm
from math import exp

def create_all_two_posible_subsecuence():
    result = {}
    letter = '0123456789abcdefghirstuvwxyzABCDEFGHIRSTUVWXYZ.,+*'
    #letter = 'abcdefghirstuvwxyzABCDEFGHIRSTUVWXYZ.,+*'
    for i in range(0, len(letter)):
        for j in range(0, len(letter)):
            tuple = letter[i] + letter[j]
            result[tuple] = 0
    return result


def secuence_learning_trainer(path):
    lines = fm.readAllLine(path)
    count = 0 #variable para no usar la primera linea
    graph = create_all_two_posible_subsecuence()
    for line in lines:
        if count != 0:
            text = line.split('|')
            state = fm.clear_text(text[1], '"', '')
            label = fm.clear_text(text[2], '"', '')
            for i in range(0, len(state)-1):
                tuple = state[i] + state[i+1]
                if tuple in graph:
                    graph[tuple] += 1 if label == 'Botnet' else -1
        count += 1
    return graph

def sigmoid(z):
    z *= -1.0
    return 1.0/(1.0 + exp(z))

def secuence_learning_testing(path, graph):
    lines = fm.readAllLine(path)
    fileName = 'labeling_result.txt'
    fileResult = open(path + os.sep + fileName, 'w')
    fileResult.write("State|CurrentLabel|LabelResult\n")
    count = 0 #variable para no usar la primera linea
    z = 0
    flag = ''
    fp = tp = fn = tn = 0
    for line in lines:
        if count != 0:
            text = line.split('|')
            state = fm.clear_text(text[1], '"', '')
            label = fm.clear_text(text[2], '"', '')
            flag = ''
            for i in range(0, len(state)-1):
                tuple = state[i] + state[i+1]
                z += graph[tuple] if tuple in graph else 0
                if tuple in graph and graph[tuple] > 0:
                    flag = 'bot'
            result = z #sigmoid(z)
            if flag == '':
                fileResult.write(state + '|' + label + '|' + 'Normal\n')
                tn += 1.0 if 'Normal' == label else 0
                fn += 1.0 if 'Normal' != label else 0
            else:
                fileResult.write(state + '|' + label + '|' + 'Botnet\n')
                tp += 1.0 if 'Botnet' == label else 0
                fp += 1.0 if 'Botnet' != label else 0
        count += 1

    total = tp + tn + fp + fn
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = (2 * precision * recall) / (precision + recall)
    accuracy = (tp + tn) / total

    print 'tp: ' + str(tp) + '----' + 'fp: ' + str(fp)
    print 'tn: ' + str(tn) + '----' + 'fn: ' + str(fn)
    print '-------------------------------------------'
    print 'Total: ' + str(total)
    print 'Precision: ' + str(precision)
    print 'Recall: ' + str(recall)
    print 'F1 Score: ' + str(F1)
    print 'Accuracy: ' + str(accuracy)
    print 'testing done'

def secuence_learning_algorithm(path_train, path_test):
    graph = secuence_learning_trainer(path_train)
    secuence_learning_testing(path_test, graph)

def confution_matrix_and_metrics(path):
    lines = fm.readAllLine(path)
    count = 0
    fp = tp = fn = tn = 0
    for line in lines:
        if count != 0:
            text = line.split('|')
            #state = fm.clear_text(text[0], '"', '')
            current_label = fm.clear_text(text[1], '"', '')
            result_label = fm.clear_text(text[2], '"', '')
            if current_label == 'Botnet':
                tp += 1.0 if result_label == current_label else 0
                fn += 1.0 if result_label != current_label else 0
            if current_label == 'Normal':
                fp += 1.0 if result_label != current_label else 0
                tn += 1.0 if result_label == current_label else 0
        count += 1

    total = tp + tn + fp + fn
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    F1 = (2 * precision * recall) / (precision + recall)
    accuracy = (tp + tn) / total

    print 'tp: ' + str(tp) + '----' + 'fp: ' + str(fp)
    print 'tn: ' + str(tn) + '----' + 'fn: ' + str(fn)
    print '-------------------------------------------'
    print 'Total: ' + str(total)
    print 'Precision: ' + str(precision)
    print 'Recall: ' + str(recall)
    print 'F1 Score: ' + str(F1)
    print 'Accuracy: ' + str(accuracy)



if __name__ == "__main__":
    path_train = '/home/jorge/DataAl/train/'
    path_test = '/home/jorge/DataAl/test/'
    path_label_result = '/home/jorge/DataAl/result/'

    a = secuence_learning_trainer(path_train)
    sorted_x = sorted(a.items(), key=operator.itemgetter(1))
    list = a.keys()
    for i in range(0, len(list)):
        subSeq = list[i]
        r = a[subSeq]
        if r != 0:
            print subSeq + ' : ' + str(r)

    #print 'Evaluation'
    #secuence_learning_algorithm(path_train, path_test)
    print '----------------------------------------'
    print 'finish'