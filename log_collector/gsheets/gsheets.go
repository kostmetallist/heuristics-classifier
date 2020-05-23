package gsheets

import (
	"fmt"
	"github.com/kostmetallist/heuclassifier/log_collector/error"
	"github.com/kostmetallist/heuclassifier/log_collector/json"
	"github.com/kostmetallist/heuclassifier/log_collector/logging"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
)

func GetGoogleSheetData(secretFilePath string, 
	sheetConfigPath string) [][]string {

	logging.LCLogger.Println("getting credentials from secret file", 
		secretFilePath)
	privateKey, err := ioutil.ReadFile(secretFilePath)
	error.CheckError(err)
	logging.LCLogger.Println("preparing the token instance...")
	conf, err := google.JWTConfigFromJSON(privateKey, sheets.SpreadsheetsScope)
	error.CheckError(err)

	logging.LCLogger.Println("retrieving sheet table itself...")
	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	error.CheckError(err)

	logging.LCLogger.Println("fetching configuration from", sheetConfigPath)
	params := json.RetrieveJsonData(sheetConfigPath)
	paramsId := params["spreadsheetId"].(string)
	paramsRange := params["range"].(string)
	resp, err := srv.Spreadsheets.Values.Get(paramsId, paramsRange).Do()
	error.CheckError(err)

	if len(resp.Values) == 0 {
		logging.LCLogger.Println("got an empty table")
		return make([][]string, 0)
	} else {
		logging.LCLogger.Println("returning preprocessed google sheets data...")
		result := make([][]string, len(resp.Values))
		for i, row := range resp.Values {
			entries := make([]string, len(row))
			for j, entry := range row {
				entries[j] = fmt.Sprintf("%s", entry)
			}
			result[i] = entries
		}
		return result
	}
}
