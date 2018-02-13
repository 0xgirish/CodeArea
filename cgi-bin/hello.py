#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgitb
import os
cgitb.enable()

print('Content-Type: text/plain;charset=utf-8\r\n')

print('Hey WhatsApp\r')


os.system('javac CodeArea.java')
os.system('java CodeArea > result')

with open('result', 'r') as f:
    for line in f:
        print(line)
