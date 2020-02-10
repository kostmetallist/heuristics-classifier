package gsheets

import (
	"encoding/json"
	"fmt"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
	"os"
	"github.com/kostmetallist/heuclassifier/error"
)

func GetGoogleSheetData(secretFile string, sheetParameters string) {

	privateKey, err := ioutil.ReadFile(secretFile)
	error.CheckError(err)
	conf, err := google.JWTConfigFromJSON(privateKey, sheets.SpreadsheetsScope)
	error.CheckError(err)

	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	error.CheckError(err)

	jsonParameters, err := os.Open(sheetParameters)
	error.CheckError(err)
	defer jsonParameters.Close()

	bytes, err := ioutil.ReadAll(jsonParameters)
	error.CheckError(err)
	// params := SheetParameters{}
	var params map[string]interface{}
	err = json.Unmarshal(bytes, &params)
	error.CheckError(err)

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
