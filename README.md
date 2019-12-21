# python-scheduler
This script works like cron, running a list of jobs at specified times or intervals.
The jobs are specified in the file 'schedule'.
This is written in Python 3

## Usage
Jobs should be specified in the file 'schedule' - an [example is given in the repository](example/schedule).
Each line specifies a job to be run in the following format:  

    min hour day month shell-command  


The parameters `min`,`hour`,`day`,`month` specify when a command should be executed in three possible ways:  
    * `*` - wildcard - run at every integer value of the relevant time period  
    * `7` - specific number - run at the specified value of the relevant time period  
    * `*/2` - multiple of - run when the relevant time period is a multiple of the specified value  

For example:  

    7 */2 * * echo "Hello World!"\

will run at the 7th minute of every second hour. Note that this is done when `hour%2=0`, so it will run at 02:07, 04:07, 06:07 etc. regardless of when it is started.\

The script also supports the option `-v` or `--verbose` to log output to the command line as well as the logfile.
## Limitations

* This can only run things at specified dates/times as outlined above; it cannot run things at regular intervals from the time this script is started
* This can only schedule to a given minute; it will execute within that minute
* Execution time of all jobs is assumed to be less than a minute in total
* Piping output or redirecting output to files is not possible by adding it to the 'schedule' file

