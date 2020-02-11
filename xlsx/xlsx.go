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
	// readLinesLimitation := params["limitReadLinesTo"].(int)
	// TODO implement read lines limitation
	logging.HCLogger.Println("loading XLSX file", xlsxFilePath)
	xlsxFile, err := xlsx.OpenFile(xlsxFilePath)
	error.CheckError(err)

	result := [][]string{}
	// note: reads continiously from all the sheets presented in a document
	for _, sheet := range xlsxFile.Sheets {
		for _, row := range sheet.Rows {

			rowData := []string{}
			for _, cell := range row.Cells {
				rowData = append(rowData, cell.String())
			}
			result = append(result, rowData)
		}
	}

	logging.HCLogger.Println("returning preprocessed XLSX data")
	return result 
}
