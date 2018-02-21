<?php
header('Content-Type: text/plain');
if(isset($_POST['code'])){
	$code = $_POST['code'];
	$file = "userCode/CodeArea";
	$language = $_POST['language'];

	if($language == "php"){
		$file = $file.".php";
	}else if($language == "python3" || $language == "python2"){
		$file = $file.".py";
	}else if($language == "cpp14"){
		$file = $file.".cpp";
	}else if($language == "C"){
		$file = $file.".c";
	}else if($language == "java"){
		$file = $file.".java";
	}
	$myfile = fopen($file, "w") or die("Unable to process");

	while (! flock($myfile, LOCK_EX | LOCK_NB));

	if(flock($myfile, LOCK_EX | LOCK_NB)){
		fwrite($myfile, $code);
	}else{
		echo "Please try again later\n";
		exit();
	}

	$command = "chmod 774 userCode/*";
	system($command);

	if($language == "php"){
		$command = "php ".$file." >Output/resultCode 2>&1";
		$result = system($command);
	}else if($language == "python3"){
		$command = "python3 userCode/CodeArea.py >Output/resultCode 2>&1";
		$result = system($command);
	}else if($language == "python2"){
		$command = "python2 userCode/CodeArea.py >Output/resultCode 2>&1";
		$result = system($command);
	}else if($language == "java"){
		$command = "javac userCode/CodeArea.java 2>&1";
		system($command);
		$command = "java userCode/CodeArea >Output/resultCode 2>&1";
		system($command);
	}else if($language == "cpp14"){
		$command = "g++ userCode/CodeArea.cpp -O3 -o userCode/ans.out";
		system($command);
		$command = "userCode/ans.out >Output/resultCode 2>&1";
		$result = system($command);
		unlink('userCode/ans.out');
	}else if($language == "C"){
		$command = "gcc CodeArea.c -O3 -o ans.out";
		system($command);
		$command = "./ans.out";
		$result = system($command);
		unlink('ans.out');
	}
	fclose($myfile);
}else{
	echo 'Sorry Can not get your code';
}
?>
