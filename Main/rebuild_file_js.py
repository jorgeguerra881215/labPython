__author__ = 'root'

import os
import sys
import file_manager as fm

def rebuild(path):
    lines = fm.readAllLine(path, 'result')
    fileName = 'result.js'
    fileResult = open(path+os.sep+fileName, 'w')
    fileResult.write("var consoleLog = [];\n")
    for line in lines:
        if len(line) > 0:
            clear_line = fm.clear_text(line)
            if clear_line[:11] != 'console.log':
                fileResult.write(line)
            else:
                text_id = clear_line[13:len(clear_line)-3]
                if text_id[:16] == '_PROFILING_INFO_':
                    new_line = "if(consoleLog.indexOf('"+text_id+"') == -1){\n"+"consoleLog.push('"+text_id+"');\n"+line+"\n}\n"
                    fileResult.write(new_line)
                else:
                    fileResult.write(line)

    fileResult.close()


if __name__ == "__main__":
    args = sys.argv[1:]
    rebuild(args[0])