import os
import logging
import time
from enum import Enum
from hashlib import md5 as MD5
from random import randint
from inspect import getframeinfo, currentframe
from .Language import LANGUAGE, TWO_STEP

LOGFILE_NAME = 'judge.log'

logging.basicConfig(filename=LOGFILE_NAME, level=logging.INFO)
filename = getframeinfo(currentframe()).filename


# Enum class for error sending
# return by: Docker.execute
class Status(Enum):
	SUCCESS = 0
	TIMEOUT = 31744
	RUNTIME_ERROR = 256
	# compilation error code is not genuine
	COMPILATION_ERROR = 257
	INTERNAL_ERROR = 404
	PROBLEM_OUTPUT_NOT_FOUND = 403
	CORRECT = 1
	WRONG = -1



class Docker:
	'''
	Docker:	Initialize docker container and run program of user and destroy container
	container : string format for command to create container
	'''
	container = "docker run -d -it --network none --name {name} -v {source}:/{target} virtual_machine:latest 1>{devnull} 2>&1"
	# container_no_internet = "docker connect none {name}"
	##################################
	#    change here for devnull 	 #
	# CONTAINER_RUNTIME = os.devnull #
	##################################
	# last container id is stored in container.log
	CONTAINER_RUNTIME = 'container.log'

	def __init__(self, timeout, language_id, code, source_path, md5_result, test_case_list ,md5_name, md5_input, target_folcer):
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
			self.test_case_list = test_case_list
			self.name = md5_name
			self.input = md5_input
			#logging.info('[{}]\n\tDocker instance created'.format(time.asctime()))
		except Exception as e:
			logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
												.format(filename, getframeinfo(currentframe()).lineno, str(e))))
			exit(-1)

	def prepare(self):
		'''
		prepare: Create container for user program | from image virtual_image
		'''
		try:
			container_command = Docker.container.format(name=self.name, source=self.path, target=self.target_folder,
														devnull=Docker.CONTAINER_RUNTIME)
			# container_internet = Docker.container_no_internet.format(name=self.name)
			os.system(container_command)
			# os.system(container_internet)
			logging.info('[{}]\n\tcontainer created . . .\n{}'.format(time.asctime(), container_command))
			return True
		except Exception as e:
			logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))
			return False

	def execute(self):
		'''
		execute : to write user program to {path}/CodeArea.{extension} and run
		return : Status of programm | SUCCESS, TIMEOUT, RUNTIME_ERROR, COMPILATION_ERROR, INTERNAL_ERROR
		'''
		try:
			file_path = '{path}/CodeArea.{lang}'.format(path=self.path,
														lang=LANGUAGE[self.language_id]['extension'])
			input_path = '/{folder}/{input_md5}_{test}.in'
			output_path = '/{folder}/{output}_{test}.out'
			path = "/{}".format(self.target_folder)
			# write user.code to corrosponding CodeArea file
			with open(file_path, 'w') as fp:
				fp.write(self.code)

			# check if language is compiled or interpreted
			# if self.language_id > TWO_STEP then language is compiled
			two_step = (self.language_id > TWO_STEP)
			if not two_step:
				# interpreted languages		
				result_list = []
				for t in self.test_case_list:
					execute_command = "{command1} <{input_file} >{output} 2>&1"\
					.format(command1=LANGUAGE[self.language_id]['command1'].format(path),
						input_file=input_path.format(folder=self.target_folder, input_md5=self.input, test=t),
							output=output_path.format(folder=self.target_folder, output=self.output, test=t))
					docker_command = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
					.format(name=self.name,  timeout=self.timeout, command=execute_command)
					status = self.__execute_one_by_one(docker_command)
					result_list.append(status)

				return_val = result_list

			else:
				# compiled languages
				# command to compile
				compile_path = '/{folder}/{output}.out'.format(folder=self.target_folder,
																output=self.output)
				compile_command = "{command1} >{output} 2>&1"\
					.format(command1=LANGUAGE[self.language_id]['command1'].format(path), output=compile_path)

				# run in docker
				docker_command = "docker exec {name} sh -c '{command}'".format(name=self.name, command=compile_command)
				os.system(docker_command)

				# if compile sucess
				if os.path.isfile('{}/{}'.format(self.path, LANGUAGE[self.language_id]['binary'])):

					# command to execute binary
					result_list = []
					for t in self.test_case_list:
						execute_command = "{command2} <{input_file} >{output} 2>&1"\
							.format(command2=LANGUAGE[self.language_id]['command2'].format(path),
									input_file=input_path.format(folder=self.target_folder, input_md5=self.input, test=t),
									output=output_path.format(folder=self.target_folder, output=self.output, test=t))
						docker_command = "docker exec {name} sh -c 'timeout {timeout} {command}'"\
							.format(name=self.name,  timeout=self.timeout, command=execute_command)

						status = self.__execute_one_by_one(docker_command)
						result_list.append(status)

					return_val = result_list

				else:
					# if not success in compilation
					return_val = [Status.COMPILATION_ERROR] * len(self.test_case_list)

			# destroy docker container
			self.destroy()
			return return_val
		except Exception as e:
			logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}"
												.format(filename, getframeinfo(currentframe()).lineno, str(e))))
			self.destroy()
			# for internal error | e.g. not able to create file CodeArea
			return [Status.INTERNAL_ERROR] * len(self.test_case_list)

	def __execute_one_by_one(command):
		status = os.system(command)
		if status is 0:
			return Status.SUCCESS
		elif status >> 8 us 124:
			return Status.TIMEOUT
		else:
			return Status.RUNTIME_ERROR

	def destroy(self):
		'''
		Destroy the docker container
		'''
		try:
			stop_container = "docker container stop {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
			remove_container = "docker container rm {name} 1>{devnull} 2>&1".format(name=self.name, devnull=Docker.CONTAINER_RUNTIME)
			os.system(stop_container)
			os.system(remove_container)
			#logging.info('[{}]\n\tContainer removed'.format(time.asctime()))
		except Exception as e:
			logging.critical('[{}]\n\t{}'.format(time.asctime(), "[{} | {}] {}".format(filename, getframeinfo(currentframe()).lineno, str(e))))


def random_md5(size):
	'''
	Generate random string md5 | for security reasons
	'''
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
