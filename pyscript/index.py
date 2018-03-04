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

#TODO: Code security checks

get = cgi.FieldStorage()   #get variables from url 

language = get['lang'].value  #language of the source code submitted by user

#statrting code processing 
#NOTE: skipping code security checks

# code processing function


def code_processing(language):
    command = ''
    compil = False
    if language == 'java':
        command = 'javac /home/girish/web/practice/userCode/CodeArea.java > ../Output/resultCode 2>&1'
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
                status2 = os.system('timeout 2.0 java -cp /home/girish/web/practice/userCode/ CodeArea >../Output/resultCode 2>&1')
                os.system('rm -f ../userCode/CodeArea.class')
            if(status2 == 124):
                print("TIMEOUT")
            elif status2 == 125:
                print("INTERNAL ERROR")
            elif status2 == 126:
                print("ERROR EXECUTING PROGRAM")
            elif status2 == 127:
                print("ERROR CAN'T EXECUTE PROGRAM")

        with open('../Output/resultCode', 'r') as result:
            for line in result:
                print(line)

code_processing(language)
