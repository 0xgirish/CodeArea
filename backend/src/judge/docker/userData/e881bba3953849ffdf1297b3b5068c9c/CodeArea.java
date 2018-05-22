// This is your CodeArea

/*
*  Don't change public class name --CodeArea--
*  Don't add package name
*/

public class CodeArea {

	public static void main (String[] args) {
        System.out.println(fun());
	}
	
	static int fun(){
	    static int x = 10;
	    return x--;
	}
}