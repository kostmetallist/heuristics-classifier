# Log Collector module

### Description
This golang module is designed for data extraction from event logs in the 
following formats:

* CSV
* Google spreadsheets data
* XLSX

After the parsing and simple processing, data is exported into JSON format 
and conveyed straight to the heuristics engine for further analysis. For the 
exported data, a temporary file is created, which will remain in the filesystem 
until all the processing is done.

### Building 
This module is generally called from the project
Use either the simplified `go run` to directly execute a program or `go build` 
command to generate an executable for deferred launch. One may want to choose 
from two commands listed below assuming `launch.go` represents an entry point 
which should be used as an argument for `go run` expression: 

* `go run launch.go`
* `go build -o launch`

### Cleaning out
If you have followed instructions to build an executable, merely do `go clean` 
while in `heuristics-classifier/log_collector`.
