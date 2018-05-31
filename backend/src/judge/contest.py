# -*- coding: UTF-8 -*-

import json
import sys
import logging
import time
import os
import filecmp
from inspect import getframeinfo, currentframe
from .Docker import Docker, random_md5, LOGFILE_NAME, Status
from .PATH import PATH as path
from django.http import HttpResponse
from problems.models import Problem, TestCase
from submissions.models import ContestSubmission, ContestSubmissionTasks
from .Language import get_code_by_name as lang_code
from django.conf import settings
from contests.models import Participant, ContestsHaveProblems
from django.db.models import Sum
from django.utils import timezone


logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


class JudgeContest:

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

            self.instance = ContestSubmission.objects.get(pk = submission_id)
            if self.instance.status != "R":
                self.is_exist = True
            else:
                self.is_exist = False
            problem = self.instance.problem.problem
            self.code = self.instance.code
            self.problem = problem.problem_code
            # time limit(in second) and memory_limit ( in bytes)
            self.timeout = float(problem.time_limit)
            self.memory_limit = int(problem.memory_limit * 1024 * 1024)
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

            self.path = path
            self.md5_name = random_md5(level)
            self.md5_input = random_md5(level)
            self.md5_result = random_md5(level)
            self.problem_output_not_found = []
            if target_folder is None:
                self.target_folder = random_md5(level)
            else:
                self.target_folder = target_folder

            # logging info
            logging.info('[{}]\n\tJudge instance created'.format(time.asctime()))
        except Exception as e:
            #logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))
            logging.critical("\n\nCritical: ", str(time.asctime()), "\n\t(file, line) = (", filename, ", ", getframeinfo(currentframe()).lineno,")\n\t", str(e), "\n\n")
            exit(-1)

    def prepare_envior(self, path=settings.MEDIA_ROOT):
        '''
        :return : boolean value
        '''
        try:
            # creating input file copy md5
            for t in self.testcase:
                static_input_path = "{}/{}/{}.in".format(path, self.problem, t)
                # mkdir userData/md5_folder
                os.system("mkdir {}".format(self.path))
                with open(static_input_path, 'r') as fp:
                    data = fp.read()

                with open('{}/{}_{}.in'.format(self.path, self.md5_input, t), 'w') as fp:
                    fp.write(data)
                # del data
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

            result_list = []
            # print(result," " ,getframeinfo(currentframe()).lineno)
            for res, test in zip(result, self.testcase):
                if res.name == 'COMPILATION_ERROR':
                    self.instance.status = 'CE'
                    judge.instance.score = 0
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

        # For total score of the problem submission
        scores = 0
        weight = 0

        for res, test_id in zip(result, self.testcase_id):
            subtask = ContestSubmissionTasks()
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
                scores = scores + subtask.testcase.weight
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
            weight = weight + subtask.testcase.weight
            subtask.save()
        if is_ac:
            self.instance.status = 'AC'
        elif is_wa:
            self.instance.status = 'WA'
        elif is_tle:
            self.instance.status = 'TLE'
        elif is_re:
            self.instance.status = 'RE'

        current_score = (scores/weight)*100 if weight>0 else 100
        max_instance = ContestSubmission.objects.filter(user = self.instance.user, problem = self.instance.problem).order_by('-score')[0]
        self.instance.score = current_score
        current_score = current_score/100
        self.instance.save()


        current_time = timezone.now()

        if self.instance.problem.contest.end_contest > current_time:
            # Contest is ON
            participant = Participant.objects.get(id = self.instance.user.id)
            # print(participant.user.user.username)
            score_to_add = 0 if current_score < max_instance.score else (current_score - max_instance.score )

            cur_weight = max_instance.problem.weight
            # print(participant.points, score_to_add, max_instance.score, current_score)
            participant.points = participant.points + cur_weight*score_to_add
            participant.save()

        # print("Score Updated")
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

    def get_problem(self):
        return self.problem, self.problem_output_not_found


    def remove_directory(self):
        '''
        remove directory from userData after getting user code output_string
        '''
        os.system("rm -rf {}".format(self.path))
        logging.info('[{}]\n\tfolder {} removed'.format(time.asctime(), self.path))
        return True



def judge_main_contest(request):
    print("\n\nIn judge_main .........................\n\n")
    level = 7   # NOTE: Change level here

    PATH = path.format(random_md5(level))

    # PATH_CONTEST: path to contest parent folder
    # default value is ../backend/media_cdn
    PATH_CONTEST = ''

    judge = JudgeContest(PATH, request)
    if judge.is_exist:
        json_data = json.dumps({"result": judge.instance.status, "score":judge.instance.score})
        return HttpResponse(json_data)
    res = 0
    judge_prepare = judge.prepare_envior() if PATH_CONTEST == '' else judge.prepare_envior(PATH_CONTEST)
    if judge_prepare:
        res = judge.run()
        if isinstance(res, bool) and not res:
            judge.remove_directory()
            json_data = json.dumps({"result": "CE", "score": judge.instance.score})
            del judge
            return HttpResponse(json_data)
        else:
            judge.safe_to_remove = True
            judge.save_result(res)
            judge.remove_directory()
            json_data = json.dumps({"result": judge.instance.status, "score": judge.instance.score})
            del judge
            return HttpResponse(json_data)
    else:
        judge.save_result(is_judge_IE=True)
        judge.remove_directory()
        json_data = json.dumps({"result": "IE"})
        del judge
        return HttpResponse(json_data)
    # return HttpResponse("Hello")
