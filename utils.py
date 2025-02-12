import pandas as pd
from datetime import datetime
import pytz
from tzlocal import get_localzone

def read_logfile(filename):
    try:
        return pd.read_csv(f"Logs/{filename}", sep = " ", names = ["timestamp", "host1", "host2"],  dtype= {"timestamp":int})
    except Exception as e:
        print(f"Log file not read:{e}")

def validate_datetime_format(datetime_str):
    try:
        datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        return True
    except Exception as e:
        print(f"The datetime entered has incorrect value: {e}")
        return False

def prepare_inputs(start, end, host):
    """
    Arg: 
        start (datetime)
        end (datetime) 
        host (str)
        The input parameters are cleaned and given the right format.
    """
    try:
        local_tz = get_localzone()
        start_unix = int(pd.to_datetime(start).tz_localize(local_tz).timestamp())
        end_unix = int(pd.to_datetime(end).tz_localize(local_tz).timestamp())
        host = host.strip()
        return start_unix, end_unix, host
    except Exception as e:
        print(f"Error preparing the input parameters: {e}")
        return None

def parse_logs(start, end, host, logs):
    """
    Arg: 
        start (UNIX or datatime)
        end (UNIX or datetime) 
        host (str)
        logs (pd dataframe) 
        The log file is parsed 

        The start, end and timestampa attribute of the log dataframe must be on the same format UNIX/datatime
    Return:
        List of host names which connected with host, during the time range from start to end.
    """
    try:
        filtered_df = logs[(logs["timestamp"]>=start) & (logs["timestamp"]<=end)]
        lconector = []
        lreceiver = []
        lconector.extend(filtered_df["host2"][filtered_df["host1"]==host])
        lreceiver.extend(filtered_df["host1"][filtered_df["host2"]==host])
        return lconector, lreceiver, filtered_df
    except Exception as e:
        print(f"Error parsering the logs: {e}")

def time_range(df):
    """
    Arg: 
        df (pd dataframe) 
    Return:
        Start and end times of the log file
    """
    local_tz = get_localzone()
    maxunix = df["timestamp"].max()
    maxdt = datetime.fromtimestamp(maxunix).astimezone(local_tz)
    minunix = df["timestamp"].min()
    mindt = datetime.fromtimestamp(minunix).astimezone(local_tz)
    return maxdt, mindt