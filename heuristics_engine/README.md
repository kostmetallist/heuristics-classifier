# Heuristics Engine module

### Description
This part is responsible for inferring of domain and implicative statements and 
attributes dependencies graph retrieval. Python modules depend on a few side 
packages and hence are meant to be run inside the virtual environment. In this 
particular case, `pipenv` is utilized to manage dependencies and dispatch the 
virtual environment entry/deactivation.

### Running the engine
Root module is named `dependency_finder.py` and supposed to be invoked after 
entrance into virtual environment.

```
pipenv shell
python3 dependency_finder.py <input_json_location>
```

or 

```
pipenv run python3 dependency_finder.py <input_json_location>
```

Note that while running commands above, your current working directory should 
be `heuristics_engine`. Otherwise, a new instance of venv will be created and 
required dependencies won't be installed.

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
