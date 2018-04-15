import os
import logging
import time
from enum import Enum
from Crypto.Hash import MD5
from random import randint
from Language import LANGUAGE, TWO_STEP

LOGFILE_NAME = 'judge.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)


class Status(Enum):
    SUCCESS = 0
    TIMEOUT = 31744
    RUNTIME_ERROR = 256
    # compilation error code is not genuine
    COMPILATION_ERROR = 257


class Docker:

    container = "docker run -d -it --name {name} -v {source}:/{target} virtual_machile:latest 1>{devnull}"


    def __init__(self, timeout, language_id, code, source_path, md5_result, md5_name, md5_input, folder="judge"):
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
        self.timeout = timeout
        self.language_id = language_id
        self.code = code
        self.folder = folder
        self.path = source_path
        self.output = md5_result
        self.name = md5_name
        self.input = md5_input
        logging.info('Time:{} Docker instance created'.format(time.asctime()))

    def prepare(self):
        try:
            container_command = Docker.container.format(name=self.name, source=self.path, target=self.folder,
                                                        devnull=os.devnull)
            os.system(container_command)
            logging.info('Time:{} container created . . .\n{}'.format(time.asctime(), container_command))
            return True
        except Exception as e:
            logging.critical('Time:{}\t{}'.format(time.asctime(), str(e)))
            return False

    def execute(self):
        try:
            file_path = '/{folder}/CodeArea.{lang}'.format(folder=self.folder,
                                                                   lang=LANGUAGE[self.language_id]['extension'])
            input_path = '/{folder}/{input_md5}.in'.format(folder=self.folder, input_md5=self.input)
            output_path = '/{folder}/{output}.out'.format(folder=self.folder, output=self.output)
            path = "/{}".format(self.folder)
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
                compile_command = "{command1} >{output} 2>&1"\
                    .format(command1=LANGUAGE[self.language_id]['command1'].format(path),
                            output=output_path)
                docker_command = "docker exec {name} {command}".format(name=self.name, command=compile_command)
                status = os.system(docker_command)
                # TODO: CHECK FOR STATUS VALUE | IF SUCESS EXECUTE OUT FILE
                if os.path.isfile('userData/{}/{}'.format(self.folder, LANGUAGE[self.language_id]['binary'])):
                    execute_command = "{command2} <{input_file} >{output} 2>&1"\
                        .format(command2=LANGUAGE[self.language_id]['command2'].format(path), input_file=input_path,
                                output=output_path)
                    docker_command = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
                        .format(name=self.name,  timeout=self.timeout, command=execute_command)
                    status = os.system(docker_command)
                    if status is 0:
                        return_val = Status.SUCCESS
                    elif status>>8 is 124:
                        return_val = Status.TIMEOUT
                    else:
                        return_val = Status.RUNTIME_ERROR
                else:
                    return_val = Status.COMPILATION_ERROR
            self.destroy()
            return return_val
        except Exception as e:
            logging.critical('Time:{}\t{}'.format(time.asctime(), str(e)))

    def destroy(self):
        try:
            stop_container = "docker container stop {name} 1>{devnull}".format(name=self.name, devnull=os.devnull)
            remove_container = "docker container rm {name} 1>{devnull}".format(name=self.name, devnull=os.devnull)
            os.system(stop_container)
            os.system(remove_container)
        except Exception as e:
            logging.critical('Time:{} {}'.format(time.asctime(), str(e)))


def random_md5(size):
    try:
        universe = '0qwe1rty2uio3pas4dfg5hjk6lzx7cvb8nm9'
        rand_string = ''
        for i in range(size):
            rand_string += universe[randint(0, len(universe))]
        rand_string = rand_string.encode()

        logging.info('Time:{} random string of size {} = {}'.format(time.asctime(), size, rand_string))
        return str(MD5.new(rand_string).hexdigest())
    except Exception as e:
        logging.critical('Time:{}\t{}'.format(time.asctime(), str(e)))
        return False
