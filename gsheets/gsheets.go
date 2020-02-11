package gsheets

import (
	"fmt"
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/json"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
)

func GetGoogleSheetData(secretFilePath string, sheetConfigPath string) {

	privateKey, err := ioutil.ReadFile(secretFilePath)
	error.CheckError(err)
	conf, err := google.JWTConfigFromJSON(privateKey, sheets.SpreadsheetsScope)
	error.CheckError(err)

	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	error.CheckError(err)

	params := json.RetrieveJsonData(sheetConfigPath)
	paramsId := params["spreadsheetId"].(string)
	paramsRange := params["range"].(string)
	resp, err := srv.Spreadsheets.Values.Get(paramsId, paramsRange).Do()
	error.CheckError(err)

	if len(resp.Values) == 0 {
		fmt.Println("getGoogleSheetData: empty table")
	} else {
		fmt.Println("data retrieved: ")
		for _, row := range resp.Values {
			fmt.Println(row[0], row[1], row[2])
		}
	}
}
