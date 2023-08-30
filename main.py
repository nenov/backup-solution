import argparse
import logging
import os
import re
import sched
import time

from synchronizer import Synchronizer


def execute_synchronization(scheduler):
    """a function to schedule the next synchronization"""
    scheduler.enter(seconds, 1, execute_synchronization, (scheduler,))
    logging.info("Starting synchronization ... ")
    synchronizer.backup_folder()
    logging.info(f"Synchronization finished. Next run in {interval}. ")


# handling arguments
parser = argparse.ArgumentParser(description="Solution for folder synchronization")
parser.add_argument("source", help="Source location")
parser.add_argument("replica", help="Replica location")
parser.add_argument("log_file", help="Log file")
parser.add_argument("-interval", help="Interval (optional)", default='0s', required=False)

args = parser.parse_args()
source = args.source
replica = args.replica
log_file = args.log_file
interval = args.interval

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename=log_file, encoding='utf-8', level=logging.DEBUG)

# some input validation
if not os.path.isdir(source):
    message = f"Source location '{source}' does not exist!"
    logging.error(message)
    raise NameError(message)

elif not re.match(r"\d+[smhd]{1}\b", interval):
    message = "Interval should be a digit followed by s/m/h/d for seconds, minutes, hours or day."
    logging.error(message)
    raise NameError(message)

# transform interval into seconds
else:
    if re.match(r"\d+[d]{1}\b", interval):
        seconds = int(re.search(r'\d+', interval).group() * 24 * 60 * 60)
    elif re.match(r"\d+[h]{1}\b", interval):
        seconds = int(re.search(r'\d+', interval).group() * 60 * 60)
    elif re.match(r"\d+[m]{1}\b", interval):
        seconds = int(re.search(r'\d+', interval).group() * 60)
    else:
        seconds = int(re.search(r'\d+', interval).group())

# check if interval has been set. If not, run only once
synchronizer = Synchronizer(source=source, replica=replica, log_file=log_file)

if seconds != 0:
    my_scheduler = sched.scheduler(time.time, time.sleep)
    my_scheduler.enter(0, 1, execute_synchronization, (my_scheduler,))
    my_scheduler.run()
else:
    logging.info("Starting synchronization ... ")
    synchronizer.backup_folder()
    logging.info("Synchronization finished.")
