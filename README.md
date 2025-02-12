
To execute the code, clone this repo. If you want to create a Python virtual environment:  
```
python -m venv {env-name} #create
source venv/bin/activate #linux/macOS
{env-name}\Scripts\activate #windows
uv pip install -r requirements.txt #install all
```

## Part 1

Streamlit app where the user can parse logs from a default log file, or enter a new log file.
Input parameters are a time range and a valid hostname. 

**Directory**
- streamlit_app.py: Logic of the streamlit app.
- utils.py: Module of functions used in the streamlit app logic.

## Part 2

Script that monitors a log file to 

**Directory**
- streaminglogs.py: a script that monitors a log file once it is executed and reports some statistics once every hour. The host name, log file path, and check interval are defined at the beginning of the script. Edit the script to modify any of them, save, and execute.
- utils.py: Module of functions used in the streminglogs script.

--------------

Rest of files:
- Logs: Directory with log files and a script to generate new logs.
- Testing: Unfinished version of a streamlit app to monitor a log file in real-time using [watchdog](https://pypi.org/project/watchdog/) python library.
- process.ipynb: notebook with some analysis and testing of python functions used in the logs parsing.
- requirements.txt: python libraries installed on the project's environment.
