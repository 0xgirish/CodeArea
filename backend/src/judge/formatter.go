// Author: Girish Kumar
// Data  : 20-jun-2018

package main

import (
	"bufio"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"os"
	"strings"
)

// formatter for output and user output files to make filecmp easy

func main() {
	if len(os.Args) < 2 {
		log.Fatal(fmt.Sprintf("Usages:\t%s file-path\n", os.Args[0]))
	}

	str, err := ioutil.ReadFile(os.Args[1])
	checkErr(err)

	// string reader
	reader_string := strings.NewReader(string(str) + "\n")
	reader := bufio.NewReader(reader_string)

	// writer to same file
	fwriter, err := os.Create(os.Args[1])
	// close before exiting program
	defer fwriter.Close()
	checkErr(err)

	writer := bufio.NewWriter(fwriter)
	var line string

forloop:
	for {
		line, err = reader.ReadString('\n')
		switch {
		case err == io.EOF:
			break forloop
		case line == "\n":
			continue
		}
		checkErr(err)
		// fmt.Print(line)
		literals := strings.Fields(line)
		line = strings.Join(literals, " ") + "\n"
		writer.WriteString(line)
	}
	// fmt.Println("-------------------")
	writer.Flush()

}

func checkErr(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
