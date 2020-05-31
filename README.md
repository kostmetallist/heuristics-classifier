# Heuristics Classifier
MMXX course work project (MSU CMC, ISP RAS).

### About
This project's goal is to provide implementation for heuristic-based dependency
inference mechanisms aimed at event log data. Two modules have been developed
for multi-stage data refinement: [`Log Collector`](https://github.com/kostmetallist/heuristics-classifier/blob/master/log_collector/README.md)
and [`Heuristics Engine`](https://github.com/kostmetallist/heuristics-classifier/blob/master/heuristics_engine/README.md).

First is responsible for input unification and passing the intermediate data
representation straight to the second module. Then, specific procedures
defined in `Heuristics Engine` are presented in order to analyze log information
and generate a model of attributes' domains classes representation, which comes
as a source for further analysis.

### Running the application
`./run.sh` on Unix systems or `start.bat` on Windows.

### Input log data
Log files in CSV and XLSX formats are presented under `log_collector/resource`
directory. Please refer to [doc](https://github.com/kostmetallist/heuristics-classifier/blob/master/log_collector/README.md)
for more details on the data origin.

### Troubleshooting
Please leave your suggestions and bug reports at
[issues page](https://github.com/kostmetallist/heuristics-classifier/issues).
