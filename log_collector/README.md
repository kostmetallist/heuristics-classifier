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

### Log data
Event log files are supposed to be placed into `resource` catalog. They are 
subdivided according to the format. Non-synthetic and non-sample logs are 
gathered from open-source repositories. The following table depicts mapping 
between event log file and its origin:

| Repository  | Files  |
|---|---|
| [Correlated and uncorrelated CSV Event Logs Figshare page](https://figshare.com/articles/Event_Logs_CSV/11342063/1) | <ul><li>`1.csv`</li><li>`2.csv`</li><li>...</li><li>`9.csv`</li></ul> |
| [Rabobank Group ICT Service Desk logs collection](https://data.4tu.nl/repository/uuid:c3e5d162-0cfd-4bb0-bd82-af5268819c35) | <ul><li>`detail_change.csv`</li><li>`detail_incident.csv`</li></ul> |
| [Online Judge (RUET OJ) Kaggle Server Log Dataset](https://www.kaggle.com/shawon10/web-log-dataset/data?select=weblog.csv) | <ul><li>`weblog.csv`</li></ul> |

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
