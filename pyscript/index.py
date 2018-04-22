#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
import sys
import cgi
import logging
import time
import os
import filecmp
from inspect import getframeinfo, currentframe
from Docker import Docker, random_md5, LOGFILE_NAME, Status


print('Content-Type: text/plain;charset=utf-8\r\n')
print()


logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


class Judge:

    def __init__(self, path, timeout=2.0, level=7, target_folder=None):
        '''
        :param path: full path to mount container source
        :param level: level or size of random_md5
        :param timeout: max time limit for program
        :param folder: folder name target
        '''
        try:
            #json_data = cgi.FieldStorage()['query']

            data_dict = json.load(sys.stdin)
            # user code string
            self.code = data_dict['code']
            # custom_input value | if not custom_input then empty string
            self.custom_input = data_dict['custom_input']
            # contest code | if custom_input then empty string
            self.contest = data_dict['contest']
            # problem code | if custom_input then empty string
            self.problem = data_dict['problem']
            # normal if custom_input is present | e.g. not empty string
            self.submission = data_dict['type']
            # language id of user submission | more info: Language.py
            self.language_id = data_dict['lang_id']
            # Timeout value for program | default is 2.0 second
            # TODO: make it contest or problem sepesific
            self.timeout = timeout
            self.path = path
            self.md5_name = random_md5(level)
            self.md5_input = random_md5(level)
            self.md5_result = random_md5(level)
            self.safe_to_remove = False
            if target_folder is None:
                self.target_folder = random_md5(level)
            else:
                self.target_folder = target_folder
            # logging info
            logging.info('[{}]\n\tJudge instance created'.format(time.asctime()))
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
                                                 .format(filename, getframeinfo(currentframe()).lineno, str(e))))
            exit(-1)

    def prepare_envior(self, path='../backend/media_cdn/'):
        '''
        :return : boolean value
        '''
        try:
            # creating input file copy md5
            if self.submission == 'normal':
                os.system("mkdir {}".format(self.path))
                with open('{}/{}.in'.format(self.path, self.md5_input), 'w') as fp:
                    fp.write(self.custom_input)
            else:
                static_input_path = "{}/{}/{}.in".format(path, self.contest, self.problem)
                # mkdir userData/md5_folder
                os.system("mkdir {}".format(self.path))
                with open(static_input_path, 'r') as fp:
                    data = fp.read()

                with open('{}/{}.in'.format(self.path, self.md5_input), 'w') as fp:
                    fp.write(data)
                del data
            self.path_contest = path
            return True

        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
                                                 .format(filename, getframeinfo(currentframe()).lineno, str(e))))
            return False

    def run(self):
        '''
        : create docker instance, execute user program and check user code
        '''
        docker = Docker(self.timeout, self.language_id, self.code, self.path, self.md5_result, self.md5_name,
                        self.md5_input, self.target_folder)
        if docker.prepare():
            result = docker.execute()
            if result.name == 'SUCCESS':
                # if submission is not normal
                if self.submission.lower() != 'normal':
                    check_against = '{}/{}/{}.out'.format(self.path_contest, self.contest, self.problem)

                    output_path = '{}/{}.out'.format(self.path, self.md5_result)
                    if os.path.isfile(output_path) and os.path.isfile(check_against):
                        res = filecmp.cmp(check_against, output_path)
                        # if user output is correct then return CORRECT else WRONG
                        return Status.CORRECT if res else Status.WRONG
                    elif os.path.isfile(check_against):
                        # if correct output of problem is not present
                        return Status.PROBLEM_OUTPUT_NOT_FOUND
                    #else:
                    #    return result
                else:
                    return Status.SUCCESS
            else:
                return result
        else:
            # if not able to create docker container
            return Status.INTERNAL_ERROR

    def get_output(self):
        '''
        :return: output of the program | use only if self.submission == normal
        :out_string conatins user.code output -> compilation_error or runtime_error or output (if SUCCESS)
        '''
        #if self.submission.lower() != 'normal':
        #    self.safe_to_remove = True
        #    return ""
        with open('{}/{}.out'.format(self.path, self.md5_result), 'r') as fp:
            out_string = fp.read()
        self.safe_to_remove = True
        return out_string

    def get_submission(self):
        return self.contest, self.problem

    def remove_directory(self):
        '''
        remove directory from userData after getting user code output_string
        '''
        if(self.safe_to_remove or self.submission.lower() != 'normal'):
            os.system("rm -r {}".format(self.path))
            #logging.info('[{}]\n\tfolder {} removed'.format(time.asctime(), self.path))
            return True
        else:
            logging.warning('[{}]\n\tRemoving without get_output is not safe'.format(time.asctime()))
            return False



level = 7   # NOTE: Change level here

PATH = '/home/karan/Desktop/csp-project/Untitled/docker/userData/{}'.format(random_md5(level))

# PATH_CONTEST: path to contest parent folder
# default value is ../backend/media_cdn
PATH_CONTEST = ''


judge = Judge(PATH)
res = 0
judge_prepare = judge.prepare_envior() if PATH_CONTEST == '' else judge.prepare_envior(PATH_CONTEST)
if judge_prepare:
    res = judge.run()
else:
    res = Status.INTERNAL_ERROR

output_string = judge.get_output()
judge.remove_directory()



if res.name == 'PROBLEM_OUTPUT_NOT_FOUND':
    get_subm = judge.get_submission()
    logging.critical('[{}]\n\tcontest/problem.out [ {}/{}.out ] is not available'
                     .format(time.asctime(), get_subm[0], get_subm[1]))
    #json_data = json.dumps({"out":res})
    # TODO: REDIRECT TO SOMETHING WENT WRONG
elif res.name == 'INTERNAL_ERROR':
    # TODO: INFORM ABOUT INCEDENT
    #json_data = json.dumps({"out": res})
    # print(res.name)
    pass
else:
    # TODO: give result to user using databse entry @ Karan
    # print(res.name)
    # print('===================> Start <===================')
    # print(output_string)
    # print('===================>  end  <===================')
    pass

#print(json_data)
if(judge.submission == "normal"):
    json_data = json.dumps({"result":res.name, "output":out_string})
else:
    json_data = json.dumps({"result":res.name})

print(json_data)

del judge