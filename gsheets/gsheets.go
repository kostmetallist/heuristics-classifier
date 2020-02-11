package gsheets

import (
	"github.com/kostmetallist/heuclassifier/error"
	"github.com/kostmetallist/heuclassifier/json"
	"github.com/kostmetallist/heuclassifier/logging"
	"golang.org/x/net/context"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
	"io/ioutil"
)

func GetGoogleSheetData(secretFilePath string, 
	sheetConfigPath string) [][]interface{} {

	logging.HCLogger.Println("getting credentials from secret file", 
		secretFilePath)
	privateKey, err := ioutil.ReadFile(secretFilePath)
	error.CheckError(err)
	logging.HCLogger.Println("preparing the token instance")
	conf, err := google.JWTConfigFromJSON(privateKey, sheets.SpreadsheetsScope)
	error.CheckError(err)

	logging.HCLogger.Println("retrieving sheet table itself")
	client := conf.Client(context.TODO())
	srv, err := sheets.New(client)
	error.CheckError(err)

	logging.HCLogger.Println("fetching configuration from", sheetConfigPath)
	params := json.RetrieveJsonData(sheetConfigPath)
	paramsId := params["spreadsheetId"].(string)
	paramsRange := params["range"].(string)
	resp, err := srv.Spreadsheets.Values.Get(paramsId, paramsRange).Do()
	error.CheckError(err)

	if len(resp.Values) == 0 {
		logging.HCLogger.Println("got an empty table")
		return make([][]interface{}, 0)
	} else {
		logging.HCLogger.Println("returning preprocessed google sheets data")
		return resp.Values
	}
}
