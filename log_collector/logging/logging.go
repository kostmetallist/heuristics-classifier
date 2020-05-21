package logging

import (
	"log"
	"os"
)

var HCLogger *log.Logger

func InitLogger() {
	// stands for Heuristics Classifier Logger
	HCLogger = log.New(os.Stdout, "[HCL] ", log.Ltime | log.Lshortfile)
}
