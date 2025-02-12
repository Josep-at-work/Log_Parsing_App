import pandas as pd
import streamlit as st
from datetime import datetime
import utils as u
from tzlocal import get_localzone
#Part 2:
from collections import deque
from watchdog.events import FileSystemEventHandler
import streamingUtils as su
import threading
import time
from watchdog.observers import Observer

            
print("Page: Parse Log Stream")

if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "observer" not in st.session_state:
    st.session_state.observer = None
if "last_report" not in st.session_state:
    st.session_state.last_report = None
if "stop_event" not in st.session_state:
    st.session_state.stop_event = threading.Event()
if "targethost" not in st.session_state:
    st.session_state.targethost = ""
if "LOG_FILE" not in st.session_state:
    st.session_state.LOG_FILE = ""
if "log_buffer" not in st.session_state:
    st.session_state.log_buffer = deque()

def hourly_results_thread(target_host, log_buffer, stop_event):
    """
    Funtion that will calculated the results every full hour from the moment the monitoring is activated
    """
    while not stop_event.is_set():
        current_time = datetime.now()
        time_to_next_hour = (60 - current_time.minute)*60 - current_time.second
        minutes_left = int(time_to_next_hour)/60
        print(f"Minutes to next parsering: {minutes_left}")
        # time.sleep(time_to_next_hour)
        time.sleep(10) #10 secnods sleep for testing
        
        try:
            lconector, lreceiver, filtered_df, most_connected_host, start_time, end_time = su.parse_logs_stream(target_host, log_buffer)
            st.session_state.last_report = {
                    "hosts_connected": lconector,
                    "hosts_receiving": lreceiver,
                    "most_connected_host": most_connected_host,
                    "df": filtered_df,
                    "start_time": start_time
                }
        except Exception as e:
            print(f"Error in hourly_results_thread: {e}")
            break

st.title("Parse Log Stream")

st.write("Enter the logs path and target host")
st.session_state.LOG_FILE = st.text_input("Log File path:")
st.session_state.targethost = st.text_input("Target host name:")

if st.button("Start Monitoring" if not st.session_state.monitoring else "Stop Monitoring", type="primary"):
    if len(st.session_state.targethost) == 0 or len(st.session_state.LOG_FILE) == 0:
        st.error("Enter a valid Log file path and Host Name")
    else:
        if st.session_state.monitoring == False:
            st.session_state.monitoring = True
            st.session_state.stop_event.clear()
            # print("start monitoring")
            st.session_state.observer = su.monitor_log_file(st.session_state.LOG_FILE, st.session_state.log_buffer)
            print(st.session_state.log_buffer)
            # Store the report in session state
            threading.Thread(
                target=hourly_results_thread,
                args=(st.session_state.targethost, st.session_state.log_buffer, st.session_state.stop_event),
                daemon = True
            ).start()
            st.rerun()

        else: 
            print("Stop Monitoring")
            st.session_state.observer.stop()
            st.session_state.monitoring = False
            st.session_state.stop_event.set()
            st.rerun()

if st.session_state.monitoring:
    st.success("Monitoring started! Results will be printed every hour.")
    
if st.session_state.last_report:
    st.write("### Last Hourly Parsering")
    st.write(f"Start time of the hourly parsering: {st.session_state.last_report["start_time"]} for {st.session_state.targethost}")
    if st.session_state.last_report["df"].empty:
        st.error(f"No logs found at the hourly report from {st.session_state.last_report["start_time"]}")
    else:
        if len(st.session_state.last_report["hosts_connected"])==0:
            st.write(f"{st.session_state.targethost} did not perform any connection")
        else:
            st.write(f"{st.session_state.targethost} did connect to {"-".join(set(st.session_state.last_report["hosts_connected"]))}")
        if len(st.session_state.last_report["hosts_receiving"])==0:
            st.write(f"{st.session_state.targethost} did not receive any connection")
        else:
            st.write(f"{st.session_state.targethost} received connection from {"-".join(set(st.session_state.last_report["hosts_receiving"]))}")
        st.warning("The previous lists of hosts are unique values. Some hosts may be connected more than once.")

        st.write(f"Host with the most connections: {st.session_state.last_report["most_connected_host"]}")
else: 
    st.warning("No reports generated yet")