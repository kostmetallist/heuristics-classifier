package csv

import (
	"encoding/csv"
	"fmt"
	"github.com/kostmetallist/heuclassifier/log_collector/error"
	"github.com/kostmetallist/heuclassifier/log_collector/json"
	"github.com/kostmetallist/heuclassifier/log_collector/logging"
	"os"
	"strings"
)


func GetCsvData(configFilePath string) [][]string {

	logging.LCLogger.Println("fetching configuration from", configFilePath)
	params := json.RetrieveJsonData(configFilePath)
	csvFilePath := params["csvFileLocation"].(string)
	// limitation is applied when the value is non negative
	//readLimit := int(params["limitReadLinesTo"].(float64))

	logging.LCLogger.Println("loading CSV file", csvFilePath)
	csvFile, err := os.Open(csvFilePath)
	error.CheckError(err)
	defer csvFile.Close()
	csvReader := csv.NewReader(csvFile)

	entries, err := csvReader.ReadAll()
	error.CheckError(err)
	logging.LCLogger.Println(fmt.Sprintf("%d lines have been succesfully read", 
		len(entries)))
	for i, row := range entries {
		for j, token := range row {
			entries[i][j] = strings.TrimSpace(token)
		}
	}
	return entries
}
