import os
import logging
import time
from enum import Enum
from hashlib import md5 as MD5
from random import randint
from inspect import getframeinfo, currentframe
from Language import LANGUAGE, TWO_STEP

LOGFILE_NAME = 'judge.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


class Status(Enum):
    SUCCESS = 0
    TIMEOUT = 31744
    RUNTIME_ERROR = 256
    # compilation error code is not genuine
    COMPILATION_ERROR = 257
    INTERNAL_ERROR = 32000
    CORRECT = 1
    WRONG = -1


class Docker:

    container = "docker run -d -it --name {name} -v {source}:/{target} virtual_machine:latest 1>{devnull} 2>&1"
    ###########################
    # change here for devnull #
    ###########################
    CONTAINER_RUNTIME = 'container.log'

    def __init__(self, timeout, language_id, code, source_path, md5_result, md5_name, md5_input, target_folcer):
        '''
        :param timeout: max time limit for code execution
        :param language_id: user programming language id option on submission
        :param code: user submitted code in string
        :param source_path: path to user folder e.g. /home/$USER/temp/userData/judge
        :param md5_result: result.out file | filecmp.compare(expected_output)
        :param md5_name: container name md5
        :param md5_input: input.in for stdin program
        :param folder: folder in container e.g.  /md5_name or /app
        '''
        try:
            self.timeout = timeout
            self.language_id = language_id
            self.code = code
            self.target_folder = target_folcer
            self.path = source_path
            self.output = md5_result
            self.name = md5_name
            self.input = md5_input
            #logging.info('[{}]\n\tDocker instance created'.format(time.asctime()))
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
                                                 .format(filename, getframeinfo(currentframe()).lineno, str(e))))
            exit(-1)

    def prepare(self):
        try:
            container_command = Docker.container.format(name=self.name, source=self.path, target=self.target_folder,
                                                        devnull=Docker.CONTAINER_RUNTIME)
            os.system(container_command)
            #logging.info('[{}]\n\tcontainer created . . .\n{}'.format(time.asctime(), container_command))
            return True
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))
            return False

    def execute(self):
        try:
            file_path = '{path}/CodeArea.{lang}'.format(path=self.path,
                                                                   lang=LANGUAGE[self.language_id]['extension'])
            input_path = '/{folder}/{input_md5}.in'.format(folder=self.target_folder, input_md5=self.input)
            output_path = '/{folder}/{output}.out'.format(folder=self.target_folder, output=self.output)
            path = "/{}".format(self.target_folder)
            with open(file_path, 'w') as fp:
                fp.write(self.code)
            two_step = (self.language_id > TWO_STEP)
            if not two_step:
                execute_command = "{command1} <{input_file} >{output} 2>&1"\
                    .format(command1=LANGUAGE[self.language_id]['command1'].format(path), input_file=input_path,
                            output=output_path)
                docker_command = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
                    .format(name=self.name,  timeout=self.timeout, command=execute_command)
                status = os.system(docker_command)
                if status is 0:
                    return_val = Status.SUCCESS
                elif status >> 8 is 124:
                    return_val = Status.TIMEOUT
                else:
                    return_val = Status.RUNTIME_ERROR

            else:
                #os.system("touch {}/{}.out".format(self.path, self.output))
                compile_command = "{command1} >{output} 2>&1"\
                    .format(command1=LANGUAGE[self.language_id]['command1'].format(path), output=output_path)
                docker_command = "docker exec {name} sh -c '{command}'".format(name=self.name, command=compile_command)
                os.system(docker_command)
                if os.path.isfile('{}/{}'.format(self.path, LANGUAGE[self.language_id]['binary'])):
                    execute_command = "{command2} <{input_file} >{output} 2>&1"\
                        .format(command2=LANGUAGE[self.language_id]['command2'].format(path), input_file=input_path,
                                output=output_path)
                    docker_command = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
                        .format(name=self.name,  timeout=self.timeout, command=execute_command)
                    status = os.system(docker_command)
                    if status is 0:
                        return_val = Status.SUCCESS
                    elif status >> 8 is 124:
                        return_val = Status.TIMEOUT
                    else:
                        return_val = Status.RUNTIME_ERROR
                else:
                    return_val = Status.COMPILATION_ERROR
            self.destroy()
            return return_val
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
                                                 .format(filename, getframeinfo(currentframe()).lineno, str(e))))
            self.destroy()
            return Status.INTERNAL_ERROR

    def destroy(self):
        try:
            stop_container = "docker container stop {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
            remove_container = "docker container rm {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
            os.system(stop_container)
            os.system(remove_container)
            #logging.info('[{}]\n\tContainer removed'.format(time.asctime()))
        except Exception as e:
            logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))


def random_md5(size):
    try:
        universe = '0qwe1rty2uio3pas4dfg5hjk6lzx7cvb8nm9'
        rand_string = ''
        for i in range(size):
            rand_string += universe[randint(0, len(universe)-1)]
        rand_string = rand_string.encode()

        #logging.info('[{}]\n\trandom string of size {} = {}'.format(time.asctime(), size, rand_string))
        hash = str(MD5(rand_string).hexdigest())
        return hash
    except Exception as e:
        logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))
        return False
