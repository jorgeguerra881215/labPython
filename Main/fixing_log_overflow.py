__author__ = 'root'
#Arreglando un codigo para procesar logs.

import os
import sys
import re
from os.path import basename


def fixing_log_overflow(path):
    lines = read_all_line(path, 'result')
    file_name = 'result.js'
    file_result = open(path + os.sep + file_name, 'w')
    file_result.write("var consoleLog = [];\n")
    for line in lines:
        if len(line) > 0:
            clear_line = clear_text(line)
            if clear_line[:11] != 'console.log':
                file_result.write(line)
            else:
                text_id = clear_line[13:len(clear_line) - 3]
                if text_id[:16] == '_PROFILING_INFO_':
                    new_line = "if(consoleLog.indexOf('" + text_id + "') == -1){\n" + "consoleLog.push('" + text_id + "');\n" + line + "\n}\n"
                    file_result.write(new_line)
                else:
                    file_result.write(line)

    file_result.close()


def read_all_line(path, exclude=''):
    for file in os.listdir(path):
        if exclude != '':
            file_name = basename(file)
            if exclude not in file_name:
                with open(path + os.sep + file, 'r') as text:
                    for line in text:
                        yield line
        else:
            with open(path + os.sep + file, 'r') as text:
                for line in text:
                    yield line


def clear_text(text, token=''):
    #Remove empty spaces
    text = re.sub(" +", "", text)
    text = re.sub("\n", "", text)
    if token != '':
        text = re.sub(token, " ", text)
    return text


if __name__ == "__main__":
    args = sys.argv[1:]
    fixing_log_overflow(args[0])