package core

import (
	"fmt"
	"io/ioutil"
	"github.com/kostmetallist/heuclassifier/csv"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/gsheets"
	"github.com/kostmetallist/heuclassifier/logging"
	"github.com/kostmetallist/heuclassifier/xlsx"
	"os"
)

var dataSources = [...]string{"local CSV", "local XLSX", "google spreadsheets"}
var chosenDataSource string

func readFile2String(ch chan<- string, path string) {
	data, err := ioutil.ReadFile(path)
	error.CheckError(err)
	ch <- string(data)
}

func ProcessLogData() {

	chWelcomeMsg := make(chan string)
	go readFile2String(chWelcomeMsg, "welcome_message.txt")
	var welcomeMessage string
	welcomeMessage = <- chWelcomeMsg
	fmt.Print(string(welcomeMessage))
	
	fmt.Println("Initializing a logger instance...")
	logging.InitLogger()
	logging.HCLogger.Println("logger is configured to use the following flags:", 
		logging.HCLogger.Flags)

	fmt.Println("Please specify an event log data source.", 
		"Possible choices are:")
	for i, entry := range dataSources {
		fmt.Println(fmt.Sprintf("[%d] %s", i, entry))
	}

	var chosenDataSourceIdx int
	for isDataSourceCorrect := false; isDataSourceCorrect == false; {

		fmt.Print("Your choice: ")
		fmt.Scanf("%d", &chosenDataSourceIdx)
		if chosenDataSourceIdx < 0 || chosenDataSourceIdx >= len(dataSources) {
			fmt.Fprintln(os.Stderr, "An incorrect value has been passed.",
				"Acceptable range is", 
				fmt.Sprintf("[0-%d]", len(dataSources)-1))
			continue
		} 
		
		isDataSourceCorrect = true
		chosenDataSource = dataSources[chosenDataSourceIdx]
	}

	switch chosenDataSource {
	case "local CSV":
		var rtd RawTableData = csv.GetCsvData("csv/params.json")
		eventSequence := rtd.ToEventSequence()
		logging.HCLogger.Println(fmt.Sprintf(
			"length of event sequence retrieved: %d", len(eventSequence)))
	case "local XLSX":
		var rtd RawTableData = xlsx.GetXlsxData("xlsx/params.json")
		eventSequence := rtd.ToEventSequence()
		logging.HCLogger.Println(fmt.Sprintf(
			"length of event sequence retrieved: %d", len(eventSequence)))
	case "google spreadsheets": 
		gsheetsData := gsheets.GetGoogleSheetData("gsheets/secret.json", 
			"gsheets/params.json")
		for _, row := range gsheetsData {
			for _, elem := range row {
				fmt.Print(elem, " ")
			}
			fmt.Println()
		}
	}
}
