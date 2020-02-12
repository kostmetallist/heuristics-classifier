package xlsx

import (
	"github.com/tealeg/xlsx"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/json"
	"github.com/kostmetallist/heuclassifier/logging"
)

func GetXlsxData(configFilePath string) [][]string {

	logging.HCLogger.Println("fetching configuration from", configFilePath)
	params := json.RetrieveJsonData(configFilePath)
	xlsxFilePath := params["xlsxFileLocation"].(string)
	// limitation is applied when the value is non negative
	readLimit := int(params["limitReadLinesTo"].(float64))

	logging.HCLogger.Println("loading XLSX file", xlsxFilePath)
	xlsxFile, err := xlsx.OpenFile(xlsxFilePath)
	error.CheckError(err)

	processedLines := 0
	result := [][]string{}
	// note: reads continiously from all the sheets presented in a document
	for _, sheet := range xlsxFile.Sheets {
		for _, row := range sheet.Rows {

			if processedLines > readLimit {
				logging.HCLogger.Println("XLSX lines read limit exceeded:", 
					"reached", readLimit, "lines")
				continue
			}

			rowData := []string{}
			for _, cell := range row.Cells {
				rowData = append(rowData, cell.String())
			}
			result = append(result, rowData)
			processedLines += 1
		}
	}

	logging.HCLogger.Println("returning preprocessed XLSX data")
	return result 
}
