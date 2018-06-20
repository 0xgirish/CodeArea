// Author: Girish Kumar
// Data  : 20-jun-2018

package main

import (
	"bufio"
	// "fmt"
	"io"
	"os"
	"strings"
)

// formatter for output and user output files to make filecmp easy

func main() {
	reader := bufio.NewReader(os.Stdin)
	writer := bufio.NewWriter(os.Stdout)
	var err error = nil
	var line string
	var breakLoop bool

	for {
		line, err = reader.ReadString('\n')
		switch {
		case err == io.EOF:
			breakLoop = true
		case err != nil:
			panic(err)
		case line == "\n":
			continue
		}
		if breakLoop {
			break
		}
		// fmt.Print(line)
		literals := strings.Fields(line)
		line = strings.Join(literals, " ") + "\n"
		writer.WriteString(line)
	}
	// fmt.Println("-------------------")
	writer.Flush()

}
