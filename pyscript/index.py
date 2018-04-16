#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import json
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

    def __init__(self, path, level=7, timeout=2.0, target_folder=None):
        '''
        :param path: full path to mount container source
        :param level: level or size of random_md5
        :param timeout: max time limit for program
        :param folder: folder name target
        '''
        try:
            json_data = cgi.FieldStorage()['query']
            data_dict = json.loads('{}'.format(json_data.value))
            self.code = data_dict['code']
            self.contest = data_dict['contest']
            self.problem = data_dict['problem']
            self.submission = data_dict['type']
            self.language_id = data_dict['lang_id']
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
            #logging.info('[{}]\n\tJudge instance created'.format(time.asctime()))
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
                                                 .format(filename, getframeinfo(currentframe()).lineno, str(e))))
            exit(-1)

    def prepare_envior(self, path='../backend/media_cdn/'):
        try:
            # creating input file copy md5
            if self.submission == 'normal':
                os.system("mkdir {}".format(self.path))
            else:
                static_input_path = "{}/{}/{}.in".format(path, self.contest, self.problem)
                # mkdir userData/md5_folder
                os.system("mkdir {}".format(self.path))
                with open(static_input_path, 'r') as fp:
                    data = fp.read()

                #TODO: CHANGES ACCORDING TO INPUT_FOLDER_MD5 IN SOURCE_FOLDER_MD5
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
        docker = Docker(self.timeout, self.language_id, self.code, self.path, self.md5_result, self.md5_name,
                        self.md5_input, self.target_folder)
        if docker.prepare():
            result = docker.execute()
            if result.name == 'SUCCESS':
                if self.submission.lower() != 'normal':
                    output_path = '{}/{}/{}.out'.format(self.path_contest, self.contest, self.problem)
                    #TODO: CHANGES ACCORDING TO OUTPUT_FOLDER_MD5 IN SOURCE_FOLDER_MD5
                    check_against = '{}/{}.out'.format(self.path, self.md5_result)
                    if os.path.isfile(output_path) and os.path.isfile(check_against):
                        res = filecmp.cmp(check_against, output_path)
                        return Status.CORRECT if res else Status.WRONG
                    elif os.path.isfile(output_path):
                        return 403
                    else:
                        return result
                else:
                    return True
            else:
                return result
        else:
            return 404

    def get_output(self):
        '''
        :return: output of the program | use only if self.submission == normal
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
        #TODO: REMOVE MD5 DIRECTORIES IN docker/userData/folder_md5
        if(self.safe_to_remove or self.submission.lower() != 'normal'):
            os.system("rm -r {}".format(self.path))
            #logging.info('[{}]\n\tfolder {} removed'.format(time.asctime(), self.path))
            return True
        else:
            logging.warning('[{}]\n\tRemoving without get_output is not safe'.format(time.asctime()))
            return False

# TODO: CHANGE PATH and PATH_CONTEST
# PATH: path to docker container mount


level = 7   # NOTE: Change level here

md5_folder = random_md5(level)
PATH = '/home/girishk/web/CodeArea/docker/userData/{}'.format(md5_folder)
PATH_REL = '../docker/userData/{}'.format(md5_folder)
# PATH_CONTEST: path to contest parent folder
PATH_CONTEST = ''
judge = Judge(PATH)
res = 0
if judge.prepare_envior():
    res = judge.run()
else:
    res = 404

output_string = judge.get_output()
judge.remove_directory()



if res == 403:
    get_subm = judge.get_submission()
    logging.critical('[{}]\n\tcontest/problem.out [ {}/{}.out ] is not available'
                     .format(time.asctime(), get_subm[0], get_subm[1]))
    #json_data = json.dumps({"out":res})
    print(res)
elif res == 404:
    # TODO: REDIRECT TO SOMETHING WENT WRONG
    #json_data = json.dumps({"out": res})
    print(res)
else:
    # TODO: give result to user using databse entry @ Karan
    #start = '===================> Start <==================='
    #end = '===================>  End  <==================='
    #json_data = json.dumps({"out": "{}\n{}\n{}\n{}".format(res.name, start, output_string, end)})
    print(res.name)
    print('===================> Start <===================')
    print(output_string)
    print('===================>  End  <===================')

#print(json_data)

del judge