#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import os
import cgi

#Hilighted code is for debugging
#---------------------------
#import cgitb
#cgitb.enable()
#---------------------------

print('Content-Type: text/plain;charset=utf-8\r\n')
print()

get = cgi.FieldStorage()   #get variables from url 

language = get['language'].value  #language of the source code submitted by user
code = get['code'].value # program submitted by the user

#TODO: Code security checks


def is_program_scure(language, code):
    #security check of the user program
    if language == 'python2' or langauge == 'python3':
        pass
        


def file_saving(language, code):        # function to save user program
    file_name = '../userCode/CodeArea'  # change path according to user-id of the user e.g. ../users/$user-id$/CodeArea
    if language == 'python3' or language == 'python2':
        file_name += '.py'
    elif language == 'cpp14':
        file_name += '.cpp'
    elif language == 'C':
        file_name += '.c'
    elif language == 'java':
        file_name += '.java'
    else:
        return False
    
    with open(file_name, 'w') as userCode:
        userCode.write(code)
        return True


def code_processing(language):      # function to run user program
    command = ''
    compil = False
    if language == 'java':
        command = 'javac ../userCode/CodeArea.java > ../Output/resultCode 2>&1'
        compil = True
    elif language == 'cpp14':
        command = 'g++ -std=c++14 ../userCode/CodeArea.cpp -o ../userCode/CodeArea.out > ../Output/resultCode 2>&1'
        compil = True
    elif language == 'C':
        command = 'gcc ../userCode/CodeArea.c -o ../userCode/CodeArea.out > ../Output/resultCode 2>&1'
        compil = True
    elif language == 'python3':
        command = 'timeout 2.0 python3 ../userCode/CodeArea.py >../Output/resultCode 2>&1'
    elif language == 'python2':
        command = 'timeout 2.0 python2 ../userCode/CodeArea.py >../Output/resultCode 2>&1'
    else:
        command = False

    if command:
        status = os.system(command)
        if compil and status == 0:
            if language == 'C' or language == 'cpp14':
                status2 = os.system('timeout 2.0 ../userCode/CodeArea.out >../Output/resultCode 2>&1')
                os.system('rm -f ../userCode/CodeArea.out')
            elif language == 'java':
                status2 = os.system('timeout 2.0 java -cp ../userCode/ CodeArea >../Output/resultCode 2>&1')
                os.system('rm -f ../userCode/CodeArea.class')
            if(status2>>8 == 124):
                print("TIMEOUT")
                return
            elif status2>>8 == 125:
                print("INTERNAL ERROR")
                return
            elif status2>>8 == 126:
                print("ERROR EXECUTING PROGRAM")
                return
            elif status2>>8 == 127:
                print("ERROR CAN'T EXECUTE PROGRAM")
                return
        if status>>8 == 124:
            print("TIMEOUT")
            return
        elif status>>8 == 125:
            print("INTERNAL ERROR")
            return
        elif status>>126:
            print("ERROR IN EXECUTING PROGRAM")
            return
        elif status>>8 == 127:
            print("ERROR: CAN'T EXECUTE PROGRAM")
            return
        else:
            with open('../Output/resultCode', 'r') as result:
                for line in result:
                    print(line)
if file_saving(language, code):
    code_processing(language)
else:
    print("Sorry, Unable to recognize language or langauge is not supported")
