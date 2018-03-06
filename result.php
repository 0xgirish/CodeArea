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
	
	fclose($myfile);

	$url = "pyscript/index.py?lang=".$language;
	header("Location: ".$url);

}else{
	echo 'Sorry Can not get your code';
}
?>
