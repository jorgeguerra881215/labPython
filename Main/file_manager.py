__author__ = 'root'

import os
import re
from os.path import basename
#Recive path to folder and read whole lines in each files found it
def readAllLine(path, exclude=''):
    for file in os.listdir(path):
        if exclude != '':
            fileName = basename(file)
            if exclude not in fileName:
                with open(path+os.sep+file, 'r') as text:
                    for line in text:
                        yield line
        else:
            with open(path+os.sep+file, 'r') as text:
                for line in text:
                    yield line

def readAllLinesByFile(path,file):
    with open(path + os.sep + file, 'r') as text:
        for line in text:
            yield line

def getFiles(path, exclude = ''):
    for file in os.listdir(path):
        if exclude != '':
            filename = basename(file)
            if exclude not in filename:
                yield file
        else:
            yield file

def getFileByName(path, name):
    for file in os.listdir(path):
        fileName = basename(file)
        if fileName == name:
            yield file

def get_status(path, exclude=''):
    for line in readAllLine(path, exclude):
        if len(line)>1:
            yield line[3]

def clear_text(text, token='', substitute=" "):
    #Remove empty spaces
    text = re.sub(" +", "", text)
    text = re.sub("\n", "", text)
    if token != '':
        text = re.sub(token, substitute, text)
    return text


def readLine(path):
    for file in os.listdir(path):
        fileName = basename(file)
        if 'botnet' not in fileName:
            botnetFile = open(path+os.sep+fileName+'_botnet', 'w')
            normalFile = open(path+os.sep+fileName+'_normal', 'w')
            allFile = open(path+os.sep + fileName + '_all', 'w')
            botnetFile.write(' Label '+'|'+' State\n')
            normalFile.write(' Label '+'|'+' State\n')
            allFile.write(' Label '+'|'+'S1|'+'S2|'+'S3|'+'S4|'+'S5|'+'S6|'+'S7|'+'S8|'+'S9|'+'S10\n')
            with open(path+os.sep+file, 'r') as text:
                for line in text:
                    manageText(line, botnetFile,normalFile,allFile)
            botnetFile.close()
            normalFile.close()
    print 'done'



def manageText(text,botnetFile,normalFile,allFile):
    #Eliminar los espacios y los saltos de linea
    text = re.sub(" +", "", text)
    text = re.sub("\n", "", text)
    line = text.split('|')
    state = '\n'
    if len(line) > 1:
        state = line[3][:10]+'\n' if len(line[3])>10 else line[3]+'###########'[:10-len(line[3])]+'\n'
        state_choped = ''.join([x+'|' if idx < len(state)-2 else x for idx,x in enumerate(state)])
    if len(line) > 1 and 'Botnet' in line[1]:
        label = 'botnet '
        botnetFile.write(label + '|')
        allFile.write(label + '|')
        botnetFile.write(state)
        allFile.write(state_choped)
    if len(line) > 1 and 'Normal' in line[1]:
        label = 'normal '
        normalFile.write(label + '|')
        allFile.write(label + '|')
        normalFile.write(state)
        allFile.write(state_choped)
