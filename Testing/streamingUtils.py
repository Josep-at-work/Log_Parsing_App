from datetime import datetime, timedelta
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import utils as u
import time
import pandas as pd

def process_new_logs(log_file, log_buffer):
    """
    Args: (str) log path
    Reads log file, gives format to the log and stores it in the log buffer for the next parse
    """
    try:
        with open(log_file, "r") as file:
            new_logs = file.readlines()
            print(f"New logs detecetd: {new_logs}")
            for log in new_logs:
                formated_log = give_format(log)
                if formated_log is not None:
                    log_buffer.append(formated_log)
                    print(f"New log added{formated_log}")
    except Exception as e:
        print(f"Error at reading the new logs: {e}")

def give_format(log_line):
    """
    Args: (str) line of the log files
    Return: (dic) dictionary value with logbuffer format
    """
    try: 
        parts = log_line.strip().split()
        return{
            "timestamp": datetime.fromtimestamp(int(parts[0])),
            "host1": parts[1],
            "host2": parts[2]
        }
    except Exception as e:
        print(f"Error giving format to the log line: {e}")
        return None

def parse_logs_stream(target_host, log_buffer):
    """
    Args: 
    target_host (str) name of the host to parse
    log_buffer (deque) current list of logs 
    Return:
    lconnector, lreceiver (l) list of connector and receivers of the target host
    filtered_df (df) dataframe with the logs parsed for the last hour
    most_connected_host (str) most connection's hostname
    """
    try:
        current_time = datetime.now()
    
        #time interval
        end_time = current_time - timedelta(minutes = 5) # Here is where we take into account the 5 minutes out-of-order logs.
        start_time = end_time - timedelta(hours = 1)
        
        logs_df = pd.DataFrame(log_buffer, columns = ["timestamp", "host1", "host2"])
        lconector, lreceiver, filtered_df = u.parse_logs(start_time, end_time, target_host, logs_df)
        if len(filtered_df) > 0:
            most_connected_host = filtered_df["host1"].value_counts().idxmax()
        else: 
            most_connected_host = "No Logs"
            print("No logs for the last hour")
        
        return lconector, lreceiver, filtered_df, most_connected_host, start_time, end_time
        
    except Exception as e: 
        print(f"Error parseing the logs:{e}")
        return None, None, None, None, None, None

class LogFileHandler(FileSystemEventHandler):
        def __init__(self, callback, LOG_FILE):
            self.callback = callback
            self.LOG_FILE = LOG_FILE

        def on_modified(self, event):
            """
            Calls the callback function everytime the LOG_FILE file is modified
            """
            print(f"Observing {self.LOG_FILE} for new logs")
            if event.src_path.endswith(self.LOG_FILE): 
                print(f"Detected modification in {self.LOG_FILE}")
                self.callback()

def monitor_log_file(LOG_FILE, log_buffer):
    process_new_logs(LOG_FILE, log_buffer)
    print("start log file monitoring")
    event_handler = LogFileHandler(lambda: process_new_logs(LOG_FILE, log_buffer), LOG_FILE)
    observer = Observer()
    observer.schedule(event_handler, path = ".", recursive=False)
    observer.start()
    return observer    
        
        