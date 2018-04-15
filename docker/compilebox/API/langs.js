
var LANGS = {
    "C": [4, "text/x-csrc"],
    "C++": [3, "text/x-c++src"],
    "Java": [5, "text/x-java"],
    "Go": [2, "text/x-go"],
    "Python-2": [0, "text/x-python"],
    "Python-3" :[1, "text/x-python"],

}




var Codes = {
    "Java": "/* package whatever; // don't place package name! */\n\nimport java.io.*;\n\nclass myCode\n{\n\tpublic static void main (String[] args) throws java.lang.Exception\n\t{\n\t\t\n\t\tSystem.out.println(\"Hello Java\");\n\t}\n}",
    "C++": "#include <iostream>\nusing namespace std;\n\nint main() {\n\tcout<<\"Hello C++\"<<endl;\n\treturn 0;\n}",
    "C": "#include <stdio.h>\n\nint main(){\n\tprintf(\"Hello C\");\n\n\treturn 0;\n}",
    "Go": "package main\nimport \"fmt\"\n\nfunc main(){\n  \n\tfmt.Printf(\"Hello Go\")\n}",
    "Python-2": "print \"Hello python2\"",
    "Python-3": "print (\"Hello python3\")",

}

