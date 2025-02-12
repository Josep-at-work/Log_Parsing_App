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

print("reloaded")

page = st.sidebar.radio("Select", ["Parse Log File", "Parse Log Stream"])

if page == "Parse Log File":

    if "new_file" not in st.session_state:
        st.session_state.new_file = None
    if "file_uploaded" not in st.session_state:
        st.session_state.file_uploaded = None
        
    st.title("Pars Log File")
    # Input Parameters Example
    st.markdown("""
        ### Example Parameters for parsing the logs
    
        - **Start Datetime**: `2024-02-05 16:10:00`
        - **End Datetime**: `2024-02-05 16:10:50`
        - **Host**: `hostB`
    
        Make sure to follow the format `YYYY-MM-DD hh:mm:ss` for datetime values.
        """)
    
    # Sidebar 
    with st.sidebar:
        st.title("Input Parameters")
        start_datetime = st.text_input("Enter the start of the time range:", help = "Accepted time format: YYYY-MM-DD hh:mm:ss")
        end_datetime = st.text_input("Enter the end of the time range:", help = "Accepted time format: YYYY-MM-DD hh:mm:ss")
        host = st.text_input("Enter the host to view its connections:", placeholder = "hostA", help="Format must be host{X}")
    
    # Workflow
    st.markdown("For this test the log file is `log_test.txt`. \
        If you want to parse anoher file, upload it here:")
    
    if st.button("New File", type='secondary') and st.session_state.new_file is None:
        st.session_state.new_file = True
    
    if st.session_state.new_file is True:
        st.session_state.file_uploaded = st.file_uploader("Upload logs file:", type=['txt', 'log'])
        if st.session_state.file_uploaded is None:
            st.warning("File must containe newline-terminated, space-separated text formatted")
            st.write("File not uploaded yet")
    
    if st.session_state.new_file is True and st.session_state.file_uploaded is not None:
        print("New file read")
        logs_df = pd.read_csv(st.session_state.file_uploaded, sep = " ", names = ["timestamp", "host1", "host2"],  dtype= {"timestamp":int})
        st.success(f"{st.session_state.file_uploaded.name} uploaded")
        print(logs_df.head())
    else: 
        logs_df = u.read_logfile("log_test.txt")
    
    lastdt, firstdt = u.time_range(logs_df)
    st.sidebar.markdown(f"""
        The current log file ranges from:   
        **{firstdt}**  
        to: **{lastdt}**
        """)
    
    if start_datetime and end_datetime and host:
        start_format = u.validate_datetime_format(start_datetime)
        end_format = u.validate_datetime_format(end_datetime)
    
        if start_format and end_format:
            if st.sidebar.button("Parse logs", type="primary"):
                start_unix, end_unix, host = u.prepare_inputs(start_datetime, end_datetime, host)
                lconector, lreceiver, filtered_df = u.parse_logs(start_unix, end_unix, host, logs_df)
                if filtered_df.empty:
                        time_message = st.error(f"No logs found from {start_datetime} to {end_datetime}")
                else:
                    st.write(f"This are the logs found from {start_datetime} to {end_datetime}:")
                    st.dataframe(filtered_df)
                    if len(lconector)==0:
                        st.write(f"{host} did not perform any connection")
                    else:
                        st.write(f"{host} did connect to: {"-".join(set(lconector))}")
                    if len(lreceiver)==0:
                        st.write(f"{host} did not receive any connection")
                    else:
                        st.write(f"{host} received connection from: {"-".join(set(lreceiver))}")
                    st.warning("The previous lists of hosts are unique values. Some hosts may be connected more than once.")
        else: 
            st.sidebar.error("Please enter a correct datetime format: YYYY-MM-DD hh:mm:ss")
            st.write("Enter the input parameters in the correct format.")
    else:
        st.write("Enter the input parameters.")



    