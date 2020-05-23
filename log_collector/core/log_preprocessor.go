package core

import (
	"fmt"
	"io/ioutil"
	"github.com/kostmetallist/heuclassifier/log_collector/csv"
	"github.com/kostmetallist/heuclassifier/log_collector/error"
	"github.com/kostmetallist/heuclassifier/log_collector/gsheets"
	"github.com/kostmetallist/heuclassifier/log_collector/json"
	"github.com/kostmetallist/heuclassifier/log_collector/logging"
	"github.com/kostmetallist/heuclassifier/log_collector/xlsx"
	"os"
	"path/filepath"
)

var dataSources = [...]string{"local CSV", "local XLSX", "google spreadsheets"}
var dumpFileLocation = "output/data.json"
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
	logging.LCLogger.Println("logger is configured to use the following flags:", 
		logging.LCLogger.Flags)

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

	var rtd RawTableData
	switch chosenDataSource {
	case "local CSV":
		rtd = csv.GetCsvData("csv/params.json")
	case "local XLSX":
		rtd = xlsx.GetXlsxData("xlsx/params.json")
	case "google spreadsheets": 
		rtd = gsheets.GetGoogleSheetData("gsheets/secret.json", 
			"gsheets/params.json")
	}

	eventSequence := rtd.ToEventSequence()
	logging.LCLogger.Println(fmt.Sprintf(
			"length of retrieved event sequence: %d", len(eventSequence)))
	logging.LCLogger.Println("preparing log data to be converted to JSON...")
	json.DumpObjectToJson(dumpFileLocation, eventSequence)

	absPath, err := filepath.Abs(dumpFileLocation)
	error.CheckError(err)
	logging.LCLogger.Println("passing control to the heuristics engine...")

	println(absPath)
}
