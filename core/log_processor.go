package core

import (
	"fmt"
	"io/ioutil"
)

func readFile2String(ch chan<- string, path string) {
	data, err := ioutil.ReadFile(path)
	checkError(err)
	ch <- string(data)
}

func ProcessLogData() {

	chWelcomeMsg := make(chan string)
	go readFile2String(chWelcomeMsg, "welcome_message.txt")
	var data string
	data = <- chWelcomeMsg
	fmt.Print(string(data))

	getGoogleSheetData()
}