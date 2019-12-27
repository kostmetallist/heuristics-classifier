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


type SheetParameters struct {
	id 	       string `json:"spreadsheetId"`
	cell_range string `json:"range"`
}

func checkError(err error) { 
	if err != nil {
		panic(err)
	}
}

func getGoogleSheetData(secretFile string, sheetParameters string) {

	private_key, err := ioutil.ReadFile(secretFile)
	checkError(err)
	conf, err := google.JWTConfigFromJSON(private_key, sheets.SpreadsheetsScope)
	checkError(err)

	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	checkError(err)

	// params, err := ioutil.ReadFile(sheetParameters)
	jsonParameters, err := os.Open(sheetParameters)
	checkError(err)

	bytes, err := ioutil.ReadAll(jsonParameters)
	checkError(err)
	var params SheetParameters
	err = json.Unmarshal(bytes, &params)
	checkError(err)

	defer jsonParameters.Close()

	// spreadsheetId := "1cGgy7ecfZe-7Mcj_GKqi1AWr_HuiKrbWZRkDICCbL-Q"
	// readRange := "A2:D5"

	// resp, err := srv.Spreadsheets.Values.Get(spreadsheetId, readRange).Do()

	fmt.Println(params.id)


	resp, err := srv.Spreadsheets.Values.Get(params.id, params.cell_range).Do()
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