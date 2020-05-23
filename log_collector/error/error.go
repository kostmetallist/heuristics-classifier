package error

import (
	"github.com/kostmetallist/heuclassifier/log_collector/logging"
)

func CheckError(err error) { 
	if err != nil {
		logging.LCLogger.Panic(err)
	}
}
