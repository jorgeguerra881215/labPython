__author__ = 'root'

import os
import re

def readLine(path):
    for file in os.listdir(path):
        text=open(path+os.sep+file, 'r')
        manageText(text.read())


def manageText(text):
    #Eliminar los espacios sobrantes
    text = re.sub(" +", " ", text)
    for word in text.split('|'):
        print word