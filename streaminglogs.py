import pandas as pd
import time
import os
from datetime import datetime, timedelta
import utils as u
from tzlocal import get_localzone

LOG_FILE = "Logs/log_test2.txt"
CHECK_INTERVAL = 3600 #1h
HOST_NAME = "host1"

log_df = pd.DataFrame(columns = ["timestamp", "host1", "host2"]).astype({"timestamp":int})

def read_new_logs(log_file, last_position):
    """
    Reads the new logs added since last reading posisition.
    Args: path of log file(str) and las position(int) read in the file.
    Return: last position read(int) and data frame with the new logs read (df)
    """
    new_logs = []
    with open(log_file, "r") as f:
        f.seek(last_position)

        for line in f:
            log = line.strip().split()
            if len(log) == 3:
                new_logs.append(log)
            else:
                print(f"Wrong number of columns in {log}")

        last_position2 = f.tell() #save last position read for next reading
        new_df = pd.DataFrame(new_logs, columns = ["timestamp", "host1", "host2"]).astype({"timestamp":int})
    if last_position !=0:
        print(new_df)
    
    return last_position2, new_df

def results(lconector, lreceiver, filtered_df, interval_start, interval_end, host_name):
    """
    Prints results
    """
    if filtered_df.empty:
        print(f"No logs found with timestamp between {interval_start} to {interval_end}")
    else:
        if len(lconector)==0:
            print(f"{host_name} did not perform any connection")
        else:
            print(f"{host_name} did connect to: {"-".join(set(lconector))}")
        if len(lreceiver)==0:
            print(f"{host_name} did not receive any connection")
        else:
            print(f"{host_name} received connection from: {"-".join(set(lreceiver))}")
        
        most_connected_host = filtered_df["host1"].value_counts().idxmax()
        print(f"Most connected host is {most_connected_host}")
    

def monitor_log_file(log_file, log_df, host_name):
    """
    Monitors a log file so that when new logs are added it reads only the new ones, which are added to a dataframe. 
    Keeps executing till the execution is stop manual (ctrl+C) or when the file path is not found.
    Args: log file path (str), logs(df) which is initialized at the beginign of the execution, host name(str) host to parse.
    """
    print("Start monitoring")
    last_position = 0
    
    while True:
        
        interval_start = datetime.now() - timedelta(seconds = 3600, minutes = 5) #change 3600 by CHECK_INTERVAL
        
        if os.path.exists(log_file):
            interval_end = datetime.now() - timedelta(minutes = 5)
            print(f"checking logs from {interval_start} to {interval_end}")

            last_position, new_df = read_new_logs(log_file, last_position) # Read new logs
            print(f"Last Position: {last_position}")

            if not new_df.empty:
                log_df = pd.concat([log_df, new_df])
            else:
                print("No new logs read")

            if not log_df.empty:
                
                interval_start_unix, interval_end_unix, host_name = u.prepare_inputs(interval_start, interval_end, host_name)
                lconector, lreceiver, filtered_df = u.parse_logs(interval_start_unix, interval_end_unix, host_name, log_df)
                if not filtered_df.empty:
                    print(f"Logs for the current time interval: {filtered_df}")
                    
                results(lconector, lreceiver, filtered_df, interval_start, interval_end, host_name)

                log_df = log_df[log_df["timestamp"]>=interval_end_unix] #During the 5 min interval that we delayed the exection, there could be some logs for the next execution. This ones are stored in the log_df and parsed in the next execution.
                print(f"Some logs are stored for the next hourly log parser \n {log_df}")
                
            else:
                print("No new logs in the last hour")
            
            time.sleep(CHECK_INTERVAL)
            
        else:
            print(f"Log file {log_file} not fount")
            break
            

if __name__ == "__main__":
    monitor_log_file(LOG_FILE, log_df, HOST_NAME)
        