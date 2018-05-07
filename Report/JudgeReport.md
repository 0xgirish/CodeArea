**Report file for Judge Working**

Files Included
---
	1. Language.py
	2. Docker.py
	3. normal.py, index.py, contest.py
	4. Dockerfile

Note: Common folder for above files --> ./backend/src/judge/
So all path in in this file are relative to above mentioned path

Report
---
1. Language.py [./]:
>	This file includes LANGUAGE dictonary which has information required to compile and execute
program of the given language.
>	To add a programming language in the judge create dictonary entry in the file as specified
in the comment section of the file.

2. Docker.py [./]:
>	This file includes class Docker and function random_md5
	a. random_md5 :
		This return a random md5 string.These random string are used to assign client folder
	(information given in report of class Docker) a name and give sample input files name.

	b. Docker :
		This class is used for creating docker containers and executing client programs in
	a sandboxed enviornment.
	
	The prepare method of class is used to create docker container with random_md5 name and no
	internet connection to these containers. These containers are mounted in a folder with name
	random_md5 (docker/userData/random_md5_string).
	
	The execute method compiles and/or executes client program in the created docker container
	compile and execute instrucions for the program is selected from Language.py's dictonary.

	The execute_one_by_one method returns flags for the result. e.g.SUCCESS, RUNTIME_ERROR etc.
	
	The destroy method removes the docker container from the server when client program result
	has been obtained.
	
3. normal.py, index.py, contest.py [./]:
>	These files includes instructions to created Docker class object and execute client progam
(and  save  result and  score in  the database in  case of index.py and  contest.py) and  return
HttpResponse with a json which has finial flag and score (in case of normal.py output of client
program against custom input).
	normal.py : This file is used when there is custom run request from client side.
	index.py  : When running a problem outside of contest (or in problem section)
	contest.py: When running a problem inside a contest.
	
	Their is slight changes in above three files.
	These files were created separately because of readability.
Normal or common instructions are :
	Create random_md5 folder(mentioned in Docker class report) in directory ./docker/userData/
	Copy testcases to above folder with name ramdom_md5
	Create Docker class object
	Execute {Docker object}.prepare and {Docker object}.execute
	Return finial result of Docker object execute result.

4. Dockerfile [./docker/]:
>	This file is used to create Docker image when seeting up or updating programming languages
or adding new one.
>	To add a new language or update existing language add or update instruction to install
compiler or interpreter.

>	Please go to this [https://www.digitalocean.com/community/tutorials/docker-explained-using-dockerfiles-to-automate-building-of-images#dockerfiles] link to get more information about Dockerfile

