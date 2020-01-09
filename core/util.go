package core

import (
	"encoding/json"
	"fmt"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
	"os"
)

func checkError(err error) { 
	if err != nil {
		panic(err)
	}
}

func getGoogleSheetData(secretFile string, sheetParameters string) {

	privateKey, err := ioutil.ReadFile(secretFile)
	checkError(err)
	conf, err := google.JWTConfigFromJSON(privateKey, sheets.SpreadsheetsScope)
	checkError(err)

	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	checkError(err)

	jsonParameters, err := os.Open(sheetParameters)
	checkError(err)
	defer jsonParameters.Close()

	bytes, err := ioutil.ReadAll(jsonParameters)
	checkError(err)
	// params := SheetParameters{}
	var params map[string]interface{}
	err = json.Unmarshal(bytes, &params)
	checkError(err)

	paramsId := params["spreadsheetId"].(string)
	paramsRange := params["range"].(string)
	resp, err := srv.Spreadsheets.Values.Get(paramsId, paramsRange).Do()
	checkError(err)

	if len(resp.Values) == 0 {
		fmt.Println("getGoogleSheetData: empty table")
	} else {
		fmt.Println("data retrieved: ")
		for _, row := range resp.Values {
			fmt.Println(row[0], row[1], row[2])
		}
	}
}