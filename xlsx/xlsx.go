package xlsx

import (
	"fmt"
	"github.com/tealeg/xlsx"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/json"
)

func GetXlsxData(configFilePath string) [][]string {

	params := json.RetrieveJsonData(configFilePath)
	xlsxFilePath := params["xlsxFileLocation"].(string)

	// limitation is applied when the value is non negative
	// readLinesLimitation := params["limitReadLinesTo"].(int)
	// TODO implement read lines limitation
	fmt.Println("Loading XLSX file", xlsxFilePath, "...")
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

	return result 
}