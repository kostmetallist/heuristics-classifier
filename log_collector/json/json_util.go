package json

import (
	j "encoding/json"
	"github.com/kostmetallist/heuclassifier/log_collector/error"
	"io/ioutil"
	"os"
)

func RetrieveJsonData(filePath string) map[string]interface{} {

	file, err := os.Open(filePath)
	error.CheckError(err)
	defer file.Close()

	bytes, err := ioutil.ReadAll(file)
	error.CheckError(err)

	var result map[string]interface{}
	err = j.Unmarshal(bytes, &result)
	error.CheckError(err)

	return result
}
