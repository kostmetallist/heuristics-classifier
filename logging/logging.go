package logging

import (
	"log"
	"os"
)

// stands for Heuristics Classifier Logger
HCLogger := log.New(os.Stdout, "[HCL]", log.Ltime | log.Lshortfile)