package core

import (
	"fmt"
	"io/ioutil"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/gsheets"
)

func readFile2String(ch chan<- string, path string) {
	data, err := ioutil.ReadFile(path)
	error.CheckError(err)
	ch <- string(data)
}

func ProcessLogData() {

	chWelcomeMsg := make(chan string)
	go readFile2String(chWelcomeMsg, "welcome_message.txt")
	var data string
	data = <- chWelcomeMsg
	fmt.Print(string(data))

	gsheets.GetGoogleSheetData("gsheets/secret.json", "gsheets/params.json")
}
