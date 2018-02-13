<?php
header('Content-Type: text/plain');
if(isset($_POST['code'])){
	$code = $_POST['code'];
	$file = "CodeArea";
	$language = $_POST['language'];

	if($language == "php"){
		$file = $file.".php";
	}else if($language == "python3" || $language == "python2"){
		$file = $file.".py";
	}else if($language == "cpp14"){
		$file = $file.".cpp";
	}else if($language == "java"){
		$file = $file.".java";
	}
	$myfile = fopen($file, "w") or die("Unable to process");
	//$i = 0;
	while (! flock($myfile, LOCK_EX | LOCK_NB)){
		//if($i % 240 == 0) echo ".";
		//$i++;
	}

	if(flock($myfile, LOCK_EX | LOCK_NB)){
		fwrite($myfile, $code);
	}else{
		echo "Please try again later\n";
		exit();
	}
	if($language == "php"){
		$command = "php ".$file." 2>&1";
		$result = system($command);
		if(! $result) echo $php_errormsg;
	}else if($language == "python3"){
		$command = "python3 CodeArea.py 2>&1";
		$result = system($command);
	}else if($language == "python2"){
		$command = "python2 CodeArea.py 2>&1";
		$result = system($command);
		if(! $result) echo $php_errormsg;
	}else if($language == "java"){
		$command = "javac CodeArea.java 2>&1";
		system($command);
		$command = "java CodeArea 2>&1";
		system($command);
	}else if($language == "cpp14"){
		$command = "g++ CodeArea.cpp -O3 -o ans.out";
		echo(exec($command));
		$command = "./ans.out";
		$result = system($command);
		echo($result);
	}
	fclose($myfile);
}else{
	echo 'Sorry Can not get your code';
}
?>
