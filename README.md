
To execute the code, clone this repo. If you want to create a Python virtual environment:  
```
python -m venv {env-name} #create
source venv/bin/activate #linux/macOS
{env-name}\Scripts\activate #windows
uv pip install -r requirements.txt #install all
```

## Part 1

Log Parsing UI, [here](https://logparsingapp-8fpxwvlomwegogubwkje7x.streamlit.app/)

Streamlit app where the user can parse logs from a default log file, or enter a new log file (.txt or .log).
Input parameters are a time range and a valid hostname. Once this parameters are entered, a Pare Logs button will appear to execute the parsing. Results will be shown in the main page.

**Directory**
- streamlit_app.py: Logic of the streamlit app.
- utils.py: Module of functions used in the streamlit app logic.

## Part 2: Log Monitoring Script

The main script is designed to monitor a log file for new entries, parse the logs, and provide insights into the connections made by a specified host. It continuously checks the log file at regular intervals(batch processing), processes new logs, and prints relevant information about the connections. The host name, log file path, and check interval are defined at the beginning of the script. Edit the script to modify any of them, save, and execute.

Default variable values: 
- log file: `log_test2.txt`
- host name: `host1`
- check interval: `1h`

### How It Works
Initialization: The script initializes an empty DataFrame (log_df) to store the logs.  
Monitoring: The script enters a loop where it continuously checks the log file for new entries.  
Reading Logs: It reads only the new logs added since the last read operation. The last read position of the file is stored for the next checking.
Processing Logs: The new logs are appended to the DataFrame, and the script filters logs within a specific time interval. This is necessary to avoid old logs. Also, due to the 5-minute delay some logs can suffer, and the time range used to execute the parsing is also delayed 5 minutes. Hence, during this 5-minute interval, some new logs can read from the file, yet they shouldn't be parsed in the current execution. These logs are filtered and stored for the next execution. 
Analyzing Connections: The script analyzes the connections made by the specified host and prints the results.  
Sleep: The script waits for a specified interval (CHECK_INTERVAL) before checking the log file again.  

**Directory**
- streaminglogs.py: Main script. The script runs indefinitely until manually stopped or if the log file is not found.
- utils.py: Module of functions used in the streminglogs script.

--------------

Rest of files:
- Logs: Directory with log files and a script to generate new logs.
- Testing: Unfinished version of a streamlit app to monitor a log file in real-time using [watchdog](https://pypi.org/project/watchdog/) python library.
- process.ipynb: notebook with some analysis and testing of python functions used in the logs parsing.
- requirements.txt: python libraries installed on the project's environment.

--------------

## Solution Diagrams

Part 1:

![image](https://github.com/user-attachments/assets/eb5c2cb9-db32-4289-9d68-72a867515e12)

