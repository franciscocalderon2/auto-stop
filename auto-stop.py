import boto3
import time
import os 
import json 
import getopt
import sys

# Usage
usageInfo = """Usage:
This scripts checks if a notebook is idle for X seconds if it does, it'll stop the notebook:
python autostop.py --time <time_in_seconds> [--port <jupyter_port>] [--ignore-connections]
Type "python autostop.py -h" for available options.
"""

# Help info
helpInfo = """-t, --time
    Auto stop time 
-c --ignore-connections
    Stop notebook once idle, ignore connected users
-h, --help
    Help information

-tz, --time-zone
"""


def get_notebook_name():
    log_path = '/opt/ml/metadata/resource-metadata.json'
    with open(log_path, 'r') as logs:
        _logs = json.load(logs)
    return _logs['ResourceName']

try:
    opts, args = getopt.getopt(sys.argv[1:], "h:t:c::tz", ["help","time=","ignore-connections", "time-zone"])
    if len(opts) == 0:
        raise getopt.GetoptError("No input parameters!")
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(helpInfo)
            exit(0)
        if opt in ("-t", "--time"):
            shut_off_time = int(arg)
        if opt in ("-p", "--port"):
            port = str(arg)
        if opt in ("-c", "--ignore-connections"):
            ignore_connections = True
        if opt in ("-tz", "--time-zone"):
            time_zone = str(arg)

except getopt.GetoptError:
    print(usageInfo)
    exit(1)


# 24 hour format 
cur=time.time()
os.environ["TZ"]=time_zone
time.tzset()

t = time.localtime(cur)
print(t)
if t.tm_hour == shut_off_time:
    # shut off instance
    client = boto3.client('sagemaker')
    client.stop_notebook_instance(
        NotebookInstanceName=get_notebook_name()
    )
