# rename_files

## Context

### What Script Does?
This script has one job. Rename files that contain spaces (a delimiter). 

`rename_files` makes the mass-renaming process more convenient; it walks from a root path and traverses the in-scope filesystem. 

*⚠️ Walking from (root) '/' will change names of all evaluated files. This may break things. Also: script script runs with `dry-mode-on` by default. Walking from root is discouraged. Target specific directories.*

### How Files Are Renamed?
* Directories renamed with an underscore, `_`.
* Non-directories renamed with a hyphen, `-`.
*🚧 adding re-naming constructs to configuration (or as arg, whichever is built first|best)*

### Use Case
* Original
    - There are too many files on your system named like "my file has spaces". Manually renaming them would be tedious.
* Ideal
    - You need to rename files non-sequentially.
* Unintended
    - Renaming certain files affecting the programs which were looking for that file. In a way, running this script could derail a system (which would be annoying because the file the prgram is looking for is in the same location, technically (the file was renamed not moved). For this reason: 
        + File/group permissions should be observed. 
        + Use the log in order to re-trace your steps. 
        + Run in `test_env`if unsure
        + `dry-run-on` is your friend.

*On test runs, many files (especially application, content, and system-like files) were found to be in (opiniated) naming violation. I found over 2000 instances in one directory.*

## Installations
* Clone the repository
    - `git clone <link-to-this-repo>`
* Change into the repo
    - `cd <path-to-cloned-repo>`

## Running the script
* One-time use
    - `python rename_files.py <dry-run-on|dry-run-off> <path>`
* Periodic use
    - Setup a cronjob `crontab -e`
    - Set script to run peridically (every monday, for example)
        + (from crontab) `* * * * mon python rename_files.py <dry-run-on|dry-run-off> <path>`
    - Clean up periodically. Remove logs older than 30days every 15th day @ 10:30am
        + (from crontab) `30 10 15 * * find /tmp/*-log-*.log -mtime +30 -exec rm {} \;`

*MAJOR TIP: Running in dry-run-on mode allows you to view what would be renamed without actually having the process take place. Try before you buy. Also: dry-run does not generate a log file.*

## Examples
* Rename all files in the desktop directory
    - `python rename_files.py dry-run-on $HOME/Desktop`

## Checking the Logs
* `rename_files.py` creates a log file to display a few stats on what happened during the script run. 
* The files are: 
    - `/tmp/<timestamp>-log-files-renamed.log`
    - `/tmp/<timestamp>-log-directories-renamed.log`

To display logged files, run `cat /tmp/*-log-*-*.log`
