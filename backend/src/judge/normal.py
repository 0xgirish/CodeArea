# -*- coding: UTF-8 -*-

import json
import sys
# import cgi
import logging
import time
import os
import filecmp
from inspect import getframeinfo, currentframe
from .Docker import Docker, random_md5, LOGFILE_NAME, Status
from .PATH import PATH as path
from django.http import HttpResponse
from problems.models import Problem, TestCase
from submissions.models import Submission, SubmissionTasks
from .Language import get_code_by_name as lang_code
from django.conf import settings


logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


class JudgeNormal:

    def __init__(self, path, request, level=7, target_folder=None):
        '''
        :param path: full path to mount container source
        :param level: level or size of random_md5
        :param timeout: max time limit for program
        :param folder: folder name target
        '''
        try:
            #json_data = cgi.FieldStorage()['query']

            data = request.POST.get("submit")
            print("Data: "+str(data))

            logging.info(data)
            data_dict = json.loads(data)

            submission_id = data_dict['submission_id']
            # user code string
            self.code = data_dict['code']
            self.instance = None
            self.language_id = data_dict['lang_id']
            # custom_input value | if not custom_input then empty string
            self.custom_input = data_dict['custom_input']
            self.timeout = 2.0
            self.memory_limit = 50000
            self.path = path
            self.md5_name = random_md5(level)
            self.md5_input = random_md5(level)
            self.md5_result = random_md5(level)
            self.safe_to_remove = False
            self.problem_output_not_found = []
            if target_folder is None:
                self.target_folder = random_md5(level)
            else:
                self.target_folder = target_folder

            self.testcase = ['normal']
            # logging info
            logging.info('[{}]\n\tJudge instance created'.format(time.asctime()))
        except Exception as e:
            logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
            exit(-1)

    def prepare_envior(self, path=settings.MEDIA_ROOT):
        '''
        :return : boolean value
        '''
        try:
            # creating input file copy md5
            os.system("mkdir {}".format(self.path))
            with open('{}/{}_normal.in'.format(self.path, self.md5_input), 'w') as fp:
                fp.write(self.custom_input)

            self.path_contest = path
            return True

        except Exception as e:
            logging.critical("\n\nCritical: " + str(time.asctime()) + "\n\t(file, line) = (" + filename + ", " + getframeinfo(currentframe()).lineno +")\n\t"+  str(e) + "\n\n")
            return False

    def run(self):
        '''
        : create docker instance, execute user program and check user code
        '''
        # print(self.path)
        docker = Docker(self.timeout, self.memory_limit, self.language_id, self.code, self.path, self.md5_result, self.testcase ,self.md5_name,
                        self.md5_input, self.target_folder)
        # print("SUCCESS")
        if docker.prepare():
            result = docker.execute()
            print("RESULT:")
            print(result)
            return result
        else:
            # if not able to create docker container
            self.instance.status = 'IE'
            self.instance.save()
            return False

    def get_output(self):
        '''
        :return: output of the program | use only if self.submission == normal
        :out_string conatins user.code output -> compilation_error or runtime_error or output (if SUCCESS)
        '''
        with open('{}/{}_normal.out'.format(self.path, self.md5_result), 'r') as fp:
            out_string = fp.read()
        self.safe_to_remove = True
        return out_string

    def remove_directory(self):
        '''
        remove directory from userData after getting user code output_string
        '''
        if(self.safe_to_remove):
            os.system("rm -rf {}".format(self.path))
            logging.info('[{}]\n\tfolder {} removed'.format(time.asctime(), self.path))
            return True
        else:
            logging.warning('[{}]\n\tRemoving without get_output is not safe'.format(time.asctime()))
            return False



def judge_main_normal(request):
    print("\n\nIn judge_main .........................\n\n")
    level = 7   # NOTE: Change level here
    PATH = path.format(random_md5(level))

    # PATH_CONTEST: path to contest parent folder
    # default value is ../backend/media_cdn
    PATH_CONTEST = ''

    judge = JudgeNormal(PATH, request)
    res = 0
    judge_prepare = judge.prepare_envior() if PATH_CONTEST == '' else judge.prepare_envior(PATH_CONTEST)
    if judge_prepare:
        res = judge.run()
        output_string = judge.get_output()
        judge.remove_directory()
        print(res[0])
        json_data = json.dumps({"result":res[0].name, "output":output_string})
        del judge
        return HttpResponse(json_data)
    else:
        judge.save_result(is_judge_IE=True)
        judge.remove_directory()
        json_data = json.dumps({"result": "IE", "output":"INTERNAL ERROR"})
        del judge
        return HttpResponse(json_data)
    # return HttpResponse("Hello")
