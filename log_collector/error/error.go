package error

import (
	"github.com/kostmetallist/heuclassifier/logging"
)

func CheckError(err error) { 
	if err != nil {
		logging.HCLogger.Panic(err)
	}
}