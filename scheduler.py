# Script to run commands at regular intervals

import csv
import logging
import datetime
import time
import subprocess
import re
import sys

# open a logfile
logging.basicConfig(level=logging.DEBUG,filename='scheduler.log',format='%(asctime)s - %(levelname)s: %(message)s')
logging.info("Starting Scheduler")

# setup for command line options
verbose = False

def main():
    # read in and parse command line arguments using getopt
    global verbose
    cmd_args = sys.argv[1:]
    if '-v' in cmd_args:
        print("Verbose mode enabled: printing all logging to console")
        verbose = True
    # read jobs from 'schedule'
    jobs = []
    with open('schedule') as schedfile:
        sched_reader = csv.reader(schedfile,delimiter=" ",quotechar='"') # open schedule file
        jobs = [parse_job(row) for row in sched_reader] # parse each line and save in 'jobs' list
    if verbose:
        for job in jobs:
            print("Job added: ", job["cmd"])


    # check once a minute if these jobs should be run
    starttime = time.time()
    while True:
        if verbose:
            print("Running jobs",datetime.datetime.now())
        check_jobs(jobs)
        time.sleep(60.0 - ((time.time() - starttime)%60.0)) # sleep for the remaining 60 seconds

def check_jobs(jobs):
    # function to loop over all the parsed jobs and run them if their specified timing matches the current time

    # check month, date, hour and minute of job against the current time
    now = datetime.datetime.now()
    for job in jobs:
        runjob = False
        if match_parameter(job["mo"],now.month):
            runjob = True
            if match_parameter(job["dy"],now.day):
                runjob = True
                if match_parameter(job["hr"],now.hour):
                    runjob = True
                    if match_parameter(job["mn"],now.minute):
                        runjob = True
                    else:
                        runjob = False
                else:
                    runjob = False
            else:
                runjob = False
        else:
            runjob = False
        if runjob:
            run_job(job) 

def match_parameter(input_param,match_param):
    # this matches an input to the given parameter.
    # if input_param is an integer, check if equal to match_param. If it is *, return true. If it is */<int>, check if it divides wholly into match_param
    # this is used to either check if the timing given is an exact number, a wildcard or a multiple wildcard
    if input_param=="*":
        return True
    elif re.match("\*\/.",input_param):
        int_param = int(input_param.replace('/','').replace('*',''))
        if match_param%int_param == 0:
            return True
        else:
            return False
    elif int(input_param)==match_param:
        return True
    else:
        return False

def parse_job(jobstring) -> dict:   
    # parse string from file into a dictionary, sanitising inputs

    job = {}
    assert(len(jobstring)>=5)
    # The job is defined by one line as follows: " <minute> <hour> <day> <month> <command to execute> "
    dictnames = ["mn","hr","dy","mo"]
    dictnums = range(len(dictnames))
    for dn,i in zip(dictnames,dictnums):
        # check it is either an integer, or *
        try:
            int(jobstring[i])
        except ValueError:
            if jobstring[i] ==  "*":
                pass
            elif re.match("\*\/.",jobstring[i]):
                pass
            else:
                raise ValueError("Job is invalid")
        # assign to relevant dictionary entry
        job[dn] = jobstring[i]
    # concatenate the rest of the row into the command desired
    job["cmd"] = jobstring[4:]
    return(job)

def run_job(job):
    # simple helper function to run a specified job and log this to the file
    global verbose
    subprocess.run(job["cmd"])
    logging.info(" ".join(job["cmd"]))
    if verbose:
        print("Running job: ",job["cmd"])

if __name__ == '__main__':
    main()
