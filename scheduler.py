import csv, logging, datetime, time, subprocess, atexit

# open a logfile
logfile = open("scheduler.log","a+")
logfile.write("Starting scheduler at %s\n"%datetime.datetime.now())

def main():
    jobs = []

    # read jobs from 'schedule'
    with open('schedule') as schedfile:
        sched_reader = csv.reader(schedfile,delimiter=" ") # open schedule file
        jobs = [parse_job(row) for row in sched_reader] # parse each line and save in 'jobs' list
    # check once a minute if these jobs should be run
    starttime = time.time()
    while True:
        print("Running jobs",datetime.datetime.now())
        check_jobs(jobs)
        time.sleep(60.0 - ((time.time() - starttime)%60.0)) # sleep for the remaining 60 seconds

def check_jobs(jobs):
    now = datetime.datetime.now()
    for job in jobs:
        runjob = False
        if job["mo"] == "*" or int(job["mn"]) == now.month:
            runjob = True
            if job["dy"] == "*" or int(job["dy"]) == now.day:
                runjob = True
                if job["hr"] == "*" or int(job["hr"]) == now.hour:
                    runjob = True
                    if job["mn"] == "*" or int(job["mn"]) == now.minute:
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
    logfile.flush() 

def parse_job(jobstring) -> dict:   
    job = {}
    # The job is defined by one line as follows: " <minute> <hour> <day> <month> <day_of_week> <command to execute> "
    job["mn"] = jobstring[0] 
    job["hr"] = jobstring[1] 
    job["dy"] = jobstring[2] 
    job["mo"] = jobstring[3] 
    job["wd"] = jobstring[4] 
    job["cmd"] = ' '.join(jobstring[5:])
    return(job)

def run_job(job):
    subprocess.run(job["cmd"])
    logfile.write("%s %s\n"%(datetime.datetime.now(),job["cmd"]))

def exit_handler():
    logfile.close()
atexit.register(exit_handler)

if __name__ == '__main__':

    main()
