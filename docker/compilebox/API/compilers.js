
/*
	This file stores the compiler/interpretor details that are provided to DockerSandbox.sh	by the app.js
	The index is the key field, 
	First column contains the compiler/interpretor that will be used for translation
	Second column is the file name to use when storing the source code
	Third column is optional, it contains the command to invoke the compiled program, it is used only for compilers
	Fourth column is just the language name for display on console, for verbose error messages
	Fifth column is optional, it contains additional arguments/flags for compilers

	You can add more languages to this API by simply adding another row in this file along with installing it in your
	Docker VM.

	Credit: Osman Ali 
	Date: 3 - JUN - 2014
	*Revised on: 30th June 2014 (Added Column number 4 to display the name of languages to console)

	Changes and improvement for CodeArea by : 	Girish Kumar
*/

exports.compilerArray= [ ["python","file.py","","Python-2",""],
			 ["python3", "file.py","","Python-3",""]
			 ["\'go run\'","file.go","","Go",""],
			 ["\'g++ -o /usercode/a.out\' ","file.cpp","/usercode/a.out","C++",""],
			 ["\'gcc -o /usercode/a.out\'", "file.c","/usercode/a.out","C",""]
			 ["javac","file.java","\'./usercode/javaRunner.sh\'","Java",""],
			 ];
