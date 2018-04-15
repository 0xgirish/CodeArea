import json
import cgi
import logging
import time
import os
import filecmp
from Docker import Docker, random_md5, LOGFILE_NAME

logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)


class Judge:

    def __init__(self, path, level=7, timeout=2.0, folder=None):
        '''
        :param path: full path to mount container source
        :param level: level or size of random_md5
        :param timeout: max time limit for program
        :param folder: folder name target
        '''
        json_data = cgi.FieldStorage()['query']
        data_dict = json.loads(json_data)
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
        if folder is None:
            self.folder = random_md5(level)
        else:
            self.folder = folder
        # logging info
        logging.info('Time:{} {}'.format(time.asctime(), 'Judge instance created'))

    def prepare_envior(self, path='../backend/media_cdn/'):
        try:
            # creating input file copy md5
            if self.submission == 'normal':
                os.system("mkdir ../docker/userData/{}".format(self.folder))
            else:
                static_input_path = "{}/{}/{}.in".format(path, self.contest, self.problem)
                # mkdir userData/md5_folder
                os.system("mkdir ../docker/userData/{}".format(self.folder))
                with open(static_input_path, 'r') as fp:
                    data = fp.read()

                #TODO: CHANGES ACCORDING TO INPUT_FOLDER_MD5 IN SOURCE_FOLDER_MD5
                with open('{}/{}.in'.format(self.path, self.md5_input), 'w') as fp:
                    fp.write(data)
            self.path_contest = path
            return True

        except Exception as e:
            logging.critical('Time:{}\t{}'.format(time.asctime(), str(e)))
            return False

    def run(self):
        docker = Docker(self.timeout, self.language_id, self.code, self.path, self.md5_result, self.md5_name,
                        self.md5_input, self.folder)

        if docker.prepare():
            result = docker.execute()
            if result.name == 'SUCCESS':
                output_path = '{}/{}/{}.out'.format(self.path_contest, self.contest, self.problem)
                #TODO: CHANGES ACCORDING TO OUTPUT_FOLDER_MD5 IN SOURCE_FOLDER_MD5
                check_against = '{}/{}/{}.out'.format(self.path, self.folder, self.md5_result)
                if os.path.isfile(output_path) and os.path.isfile(check_against):
                    res = filecmp.cmp(check_against, output_path)
                    return res
                elif os.path.isfile(output_path):
                    return 403
                else:
                    return result
            else:
                return result
        else:
            return 404

    def remove_directory(self):
        #TODO: REMOVE MD5 DIRECTORIES IN docker/userData/
        pass

    def get_submission(self):
        return self.contest, self.problem

# TODO: CHANGE PATH and PATH_CONTEST
# PATH: path to docker container mount
PATH = ''
# PATH_CONTEST: path to contest parent folder
PATH_CONTEST = ''
judge = Judge(PATH)
if judge.prepare_envior(PATH_CONTEST):
    res = judge.run()
else:
    res = 404

judge.remove_directory()

if res == 403:
    get_subm = judge.get_submission()
    logging.critical('Time:{} contest/problem.out [ {}/{}.out ] is not available'
                     .format(time.asctime(), get_subm[0], get_subm[1]))
elif res == 404:
    # TODO: REDIRECT TO SOMETHING WENT WRONG
    pass
else:
    # TODO: give result to user using databse entry @ Karan
    pass