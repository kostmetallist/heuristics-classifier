package json

import (
	j "encoding/json"
	"github.com/kostmetallist/heuclassifier/log_collector/error"
	"github.com/kostmetallist/heuclassifier/log_collector/logging"
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
	logging.HCLogger.Println(filePath, "has been successfully unmarshalled")

	return result
}

func DumpObjectToJson(destinationPath string, object interface{}) {

	file, err := os.Create(destinationPath)
	error.CheckError(err)
	logging.HCLogger.Println(destinationPath, "is prepared for data dump")
	defer file.Close()

	bytes, err := j.Marshal(object)
	error.CheckError(err)
	_, err = file.Write(bytes)
	error.CheckError(err)
	logging.HCLogger.Println("data have been successfully written")
}
