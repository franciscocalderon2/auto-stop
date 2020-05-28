#!/bin/bash

set -e

# OVERVIEW
# This script stops a SageMaker notebook once it's idle for more than 1 hour (default time)
# You can change the idle time for stop using the environment variable below.
# If you want the notebook the stop only if no browsers are open, remove the --ignore-connections flag
#
# Note that this script will fail if either condition is not met
#   1. Ensure the Notebook Instance has internet connectivity to fetch the example config
#   2. Ensure the Notebook Instance execution role permissions to SageMaker:StopNotebookInstance to stop the notebook 
#       and SageMaker:DescribeNotebookInstance to describe the notebook.
#

# Hour of day to shut off 24 hour format
SHUT_OFF_TIME=18

# you can set the timezone to your location using 3 Character codes found below
# https://www.timeanddate.com/time/map/
TIME_ZONE="MST"

echo "Fetching the autostop script"
wget https://raw.githubusercontent.com/franciscocalderon2/auto-stop/master/auto-stop.py

echo "Starting the SageMaker autostop script in cron"

(crontab -l 2>/dev/null; echo "1 * * * * python $PWD/auto-stop.py --time $SHUT_OFF_TIME --time-zone $TIME_ZONE --ignore-connections") | crontab -