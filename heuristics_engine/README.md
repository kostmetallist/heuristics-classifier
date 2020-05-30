# Heuristics Engine module

### Description
This part is responsible for inferring of domain and implicative statements and 
attributes dependencies graph retrieval. Python modules depend on a few side 
packages and hence are meant to be run inside the virtual environment. In this 
particular case, `pipenv` is utilized to manage dependencies and dispatch the 
virtual environment entry/deactivation.

### Running the engine
Root module is named `engine.py` and supposed to be invoked after 
entrance into virtual environment. While running commands, your current working
directory should be `heuristics_engine`. Otherwise, a new instance of venv
will be created and required dependencies won't be installed. Use the following
lines to launch the engine:

```
pipenv shell
python3 engine.py <input_json_location> [<heuristic_name>]
```

or 

```
pipenv run python3 engine.py <input_json_location> [<heuristic_name>]
```

A `<heuristic_name>` argument is optional and has the default value of
`sequence-oriented` heuristic. Available heuristics are enumerated underneath:

| Heuristic name | Description |
|---|---|
| `sequence-oriented` (DEFAULT) | Performs numeric analysis, focusing on INTEGER and REAL trivial types. Detects monotonous sequences, alternate signs, range of values, and gives assessments on whether the attribute can be an identifier. |
| `distribution-oriented` | Provides information regarding normalization of REAL values and gives an empirical inference of values' distribution based on statistical fit for different distributions. |
| `date-oriented` | Tries to treat STRING-typed fields as a date/datetime/time entries and providing statements on conformance of the attribute to the standardized or custom date/timestamp notation. Evaluates time periods during which log records are produced and infers periodic regularities. |

As an example, one can invoke `sequence-oriented` heuristic to process generic
data created for demonstration:

```
pipenv run python3 engine.py ../log_collector/output/sample.json sequence-oriented
```

This engine is triggered automatically by Log Collector module after 
preprocessed log data had been dumped into the configured output folder 
(e.g. `log_collector/output`). Therefore, launch of this module is the part 
of workflow initiated by root level `run.sh`/`start.bat` script.

### Visualizing `.dot` files data
By default, generated graphs are placed into `output/dot_output` directory and 
are in [DOT format](https://www.graphviz.org/doc/info/lang.html). In order to 
convert these files into human-readable form, the `dot` utility can be used. For 
Linux systems, run `dot -Tpdf -o<desired-output-location> <path-to-dot-files>` 
to receive a PDF document with the underlying graph depicted.
