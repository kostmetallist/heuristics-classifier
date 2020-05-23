package logging

import (
	"log"
	"os"
)

var LCLogger *log.Logger

func InitLogger() {
	// stands for Log Collector Logger
	LCLogger = log.New(os.Stdout, "[LCL] ", log.Ltime | log.Lshortfile)
}
