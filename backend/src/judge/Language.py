# Author    :   Girish Kumar
# Date      :   15-april-2018
# Info      :   Language information


# TO add new language to judge change LANGUAGE list with proper entries

# language      id
# python 2      0
# python 3      1
# golang        2
# C             3
# Cpp           4
# java          5



# title : Name of the language (not necessary)| extension : language specific (necessary)
# command1 : necessary
# binary : necessary (in case of compiled language)
# Interpeted Language : command1 -> execution command e.g. php CodeArea.php
# Compiled Language: command1 -> command to compile program
#                    command2 -> command to execute binary
#                    binary   -> name of the binary file created after compilation


# FORMAT =   "LANGUAGE"                "Extension"      "COMMAND 1"
#               "BINARY"                "COMMAND 2"
LANGUAGE = {0: {"title": "python2", "extension": "py",  "command1": "python2 {}/CodeArea.py"},
            1: {"title": "python3", "extension": "py",  "command1": "python3 {}/CodeArea.py"},
            #############################
            #   Interpreted | compiled  #
            #############################
            2: {"title": "golang",     "extension": "go",  "command1": "go build -o {0}/CodeArea.out {0}/CodeArea.go",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            3: {"title": "C",          "extension": "c",   "command1": "gcc -O3 {0}/CodeArea.c -o {0}/CodeArea.out",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            4: {"title": "cpp14",        "extension": "cpp", "command1": "g++ -O3 {0}/CodeArea.cpp -o {0}/CodeArea.out",
                "binary": "CodeArea.out", "command2": "{}/CodeArea.out"},
            5: {"title": "java",       "extension": "java", "command1": "javac {0}/CodeArea.java",
                "binary": "CodeArea.class", "command2": "java -cp /{}/ CodeArea"}
            }



# If there is an entry for interpreted language than chagen TWO_STEP value
# TWO_STEP: --> index in the LANGUAGE after which all languages are compiled
TWO_STEP = 1



def get_code_by_name(name):
    global LANGUAGE
    name = str(name)
    for key, value in LANGUAGE.items():
        if value['title'] == name:
            return int(key)