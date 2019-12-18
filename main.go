package main

import (
	"fmt"
	"io/ioutil"
)

func checkError(err error) { 
	if err != nil {
		panic(err)
	}
}

func readFile2String(ch chan<- string, path string) {
	data, err := ioutil.ReadFile(path)
	checkError(err)
	ch <- string(data)
}

func main() {

	chWelcomeMsg := make(chan string)
	go readFile2String(chWelcomeMsg, "welcome_message.txt")
	var data string
	data = <- chWelcomeMsg
	fmt.Print(string(data))
}