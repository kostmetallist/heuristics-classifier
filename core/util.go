package core

import (
	"fmt"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
)

func checkError(err error) { 
	if err != nil {
		panic(err)
	}
}

func getGoogleSheetData() {

	private_key, err := ioutil.ReadFile("secret.json")
	checkError(err)
	conf, err := google.JWTConfigFromJSON(private_key, sheets.SpreadsheetsScope)
	checkError(err)

	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	checkError(err)

	spreadsheetID := "1cGgy7ecfZe-7Mcj_GKqi1AWr_HuiKrbWZRkDICCbL-Q"
	readRange := "Class Data!A2:D"
	resp, err := srv.Spreadsheets.Values.Get(spreadsheetID, readRange).Do()
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