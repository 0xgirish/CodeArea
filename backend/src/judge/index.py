#!/usr/bin/env python3
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


print('Content-Type: text/plain;charset=utf-8\r\n')
print()


logging.basicConfig(level=logging.INFO)
filename = getframeinfo(currentframe()).filename


class Judge:

    def __init__(self, path, request, timeout=2.0, level=7, target_folder=None):
        '''
        :param path: full path to mount container source
        :param level: level or size of random_md5
        :param timeout: max time limit for program
        :param folder: folder name target
        '''
        try:
            #json_data = cgi.FieldStorage()['query']

            data = request.POST.get("submit")
            # print("Data: "+str(data))

            logging.info(data)
            data_dict = json.loads(data)
            self.submission = data_dict['type']

            submission_id = data_dict['submission_id']
            # user code string

            if self.submission == 'normal':
                self.code = data_dict['code']
                self.instance = None
                self.language_id = data_dict['lang_id']
            else:
                self.instance = Submission.objects.get(pk = submission_id)
                problem = self.instance.problem
                self.code = self.instance.code
                self.problem = problem.problem_code
                testcases = TestCase.objects.filter(problem = problem)
                
                # testcase calculation
                self.testcase = []
                self.testcase_id = []
                for testcase in testcases:
                    testcase_file_name = testcase.input
                    testcase_file_name = str(testcase_file_name).split("/")[1].split(".")[0]
                    testcase_id = testcase.id
                    self.testcase.append(testcase_file_name)
                    self.testcase_id.append(testcase_id)
                self.language_id = lang_code(self.instance.language.language_name)


            # custom_input value | if not custom_input then empty string
            self.custom_input = data_dict['custom_input']


            self.timeout = timeout
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

            if self.submission == 'normal':
                self.testcase = ['normal']
            # logging info
            logging.info('[{}]\n\tJudge instance created'.format(time.asctime()))
        except Exception as e:
            #logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))
            print("\n\nCritical: ", str(time.asctime()), "\n\t(file, line) = (", filename, ", ", getframeinfo(currentframe()).lineno,")\n\t", str(e), "\n\n")
            exit(-1)

    def prepare_envior(self, path=settings.MEDIA_ROOT):
        '''
        :return : boolean value
        '''
        try:
            # creating input file copy md5
            if self.submission == 'normal':
                os.system("mkdir {}".format(self.path))
                with open('{}/{}_normal.in'.format(self.path, self.md5_input), 'w') as fp:
                    fp.write(self.custom_input)
            else:
                for t in self.testcase:
                    static_input_path = "{}/{}/{}.in".format(path, self.problem, t)
                    # mkdir userData/md5_folder
                    os.system("mkdir {}".format(self.path))
                    with open(static_input_path, 'r') as fp:
                        data = fp.read()

                    with open('{}/{}_{}.in'.format(self.path, self.md5_input, t), 'w') as fp:
                        fp.write(data)
                del data
            self.path_contest = path
            return True

        except Exception as e:
            print("\n\nCritical: ", str(time.asctime()), "\n\t(file, line) = (", filename, ", ", getframeinfo(currentframe()).lineno,")\n\t", str(e), "\n\n")
            return False

    def run(self):
        '''
        : create docker instance, execute user program and check user code
        '''
        # print(self.path)
        docker = Docker(self.timeout, self.language_id, self.code, self.path, self.md5_result, self.testcase ,self.md5_name,
                        self.md5_input, self.target_folder)
        # print("SUCCESS")
        if docker.prepare():
            result = docker.execute()
            print("RESULT:")
            print(result)
            if self.submission.lower() == 'normal':
                return result

            result_list = []
            # print(result," " ,getframeinfo(currentframe()).lineno)
            for res, test in zip(result, self.testcase):
                if res.name == 'COMPILATION_ERROR':
                    self.instance.status = 'CE'
                    self.instance.save()
                    return False

                if res.name == 'SUCCESS':
                    check_against = '{}/{}/{}.out'.format(self.path_contest, self.problem, test)
                    output_path = '{}/{}_{}.out'.format(self.path, self.md5_result, test)
                    if os.path.isfile(output_path) and os.path.isfile(check_against):
                        res_ = filecmp.cmp(check_against, output_path)
                        # if user output is correct then return CORRECT else WRONG
                        result_list.append(Status.CORRECT if res_ else Status.WRONG)
                    elif os.path.isfile(check_against):
                        # if correct output of problem is not present
                        self.problem_output_not_found.append(test)
                        result_list.append(Status.PROBLEM_OUTPUT_NOT_FOUND)
                else:
                    result_list.append(res)

            return result_list

        else:
            # if not able to create docker container
            self.instance.status = 'IE'
            self.instance.save()
            return False

    def save_result(self,result=None, is_judge_IE=False):
        if is_judge_IE:
            self.instance.status = 'IE'
            self.instance.save()
            return True
        is_ac = False
        is_tle = True
        is_re = True
        is_wa = True
        print(result, " ", getframeinfo(currentframe()).lineno)
        for res, test_id in zip(result, self.testcase_id):
            subtask = SubmissionTasks()
            subtask.submission = self.instance
            subtask.testcase = TestCase.objects.get(id = test_id)
            """ 
            Status options are: 
            ACCEPTED_ANSWER = 'AC'
            WRONG_ANSWER = 'WA'
            RUNTIME_ERROR = 'RE'
            TIME_EXCEEDED = 'TLE'
            INTERNAL_ERROR = 'IE'
            """
            subtask.status = self.status_code(res)
            # print("\n\n", self.status_code(res), "\n\n")
            if subtask.status == 'AC':
                is_ac = True
                is_tle = False
                is_re = False
                is_wa = False
            elif subtask.status == 'WA' and is_wa:
                is_re = False
                is_tle = False
            elif subtask.status == 'TLE' and is_tle:
                is_wa = False
                is_re = False
            elif subtask.status == 'RE' and is_re:
                is_wa = False
                is_tle = False
            # save the instance
            subtask.save()
        if is_ac:
            self.instance.status = 'AC'
        elif is_wa:
            self.instance.status = 'WA'
        elif is_tle:
            self.instance.status = 'TLE'
        elif is_re:
            self.instance.status = 'RE'
        self.instance.save()
        return True

    def status_code(self, status):
        if status.name == 'CORRECT':
            return 'AC'
        elif status.name == 'WRONG':
            return 'WA'
        elif status.name == 'RUNTIME_ERROR':
            return 'RE'
        elif status.name == 'TIMEOUT':
            return 'TLE'
        else:
            return 'IE'
        

    def get_output(self):
        '''
        :return: output of the program | use only if self.submission == normal
        :out_string conatins user.code output -> compilation_error or runtime_error or output (if SUCCESS)
        '''
        if self.submission.lower() != 'normal':
           self.safe_to_remove = True
           return ""
        with open('{}/{}_normal.out'.format(self.path, self.md5_result), 'r') as fp:
            out_string = fp.read()
        self.safe_to_remove = True
        return out_string

    
    def get_problem(self):
        return self.problem, self.problem_output_not_found
    

    def remove_directory(self):
        '''
        remove directory from userData after getting user code output_string
        '''
        if(self.safe_to_remove):
            os.system("rm -rf {}".format(self.path))
            print('[{}]\n\tfolder {} removed'.format(time.asctime(), self.path))
            return True
        else:
            print('[{}]\n\tRemoving without get_output is not safe'.format(time.asctime()))
            return False



def judge_main(request):

    level = 7   # NOTE: Change level here

    PATH = path.format(random_md5(level))

    # PATH_CONTEST: path to contest parent folder
    # default value is ../backend/media_cdn
    PATH_CONTEST = ''


    judge = Judge(PATH, request)
    res = 0
    judge_prepare = judge.prepare_envior() if PATH_CONTEST == '' else judge.prepare_envior(PATH_CONTEST)
    if judge_prepare:
        res = judge.run()
        if isinstance(res, bool) and not res:
            judge.remove_directory()
            del judge
            return HttpResponse("CE")
        elif judge.submission == 'normal':
            output_string = judge.get_output()
            judge.remove_directory()
            print(res[0])
            json_data = json.dumps({"result":res[0].name, "output":output_string})
            del judge
            return HttpResponse(json_data)
        else:
            judge.safe_to_remove = True
            judge.save_result(res)
            judge.remove_directory()
            del judge
            return HttpResponse(self.instance.status)
    else:
        judge.save_result(is_judge_IE=True)
        judge.remove_directory()
        return HttpResponse("IE")
    # return HttpResponse("Hello")

    # if res.name == 'PROBLEM_OUTPUT_NOT_FOUND':
    #     get_subm = judge.get_submission()
    #     logging.critical('[{}]\n\tfor problem {} some test case output is missing | '
    #                      .format(time.asctime(), get_subm[0]), *get_subm[1])
    #     #json_data = json.dumps({"out":res})
    #     # TODO: REDIRECT TO SOMETHING WENT WRONG
    # elif res.name == 'INTERNAL_ERROR':
    #     # TODO: INFORM ABOUT INCEDENT
    #     #json_data = json.dumps({"out": res})
    #     # print(res.name)
    #     pass
    # else:
    #     # TODO: give result to user using databse entry @ Karan
    #     # print(res.name)
    #     # print('===================> Start <===================')
    #     # print(output_string)
    #     # print('===================>  end  <===================')
    #     pass
