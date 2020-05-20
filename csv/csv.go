package csv

import (
	"encoding/csv"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/json"
	"github.com/kostmetallist/heuclassifier/logging"
	"os"
)


func GetCsvData(configFilePath string) [][]string {

	logging.HCLogger.Println("fetching configuration from", configFilePath)
	params := json.RetrieveJsonData(configFilePath)
	csvFilePath := params["csvFileLocation"].(string)
	// limitation is applied when the value is non negative
	//readLimit := int(params["limitReadLinesTo"].(float64))

	logging.HCLogger.Println("loading CSV file", csvFilePath)
	csvFile, err := os.Open(csvFilePath)
	error.CheckError(err)
	csvReader := csv.NewReader(csvFile)

	entries, err := csvReader.ReadAll()
	error.CheckError(err)
	logging.HCLogger.Println("%d lines have been succesfully read", len(entries))
	return entries
}
