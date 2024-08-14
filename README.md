# rename_files

## Context

### What Script Does?
This script has one job. Rename files that contain spaces. 
Renaming renaming makes looking for files a more convenient process. It will walk from the root path and traverse the entire filesystem (run in background for silence). 

*FYI: Walking from / will change names of all files found. This may break things. The script runs in dry mode by default.*

### How Files Are Renamed?
* Directories renamed with an underscore, `_`.
* Non-directories renamed with a hyphen, `-`.

### Use Case
You have too many files on your system named like "my file has spaces".
*On test runs, many files (especially application and system-like files) were found to be in naming violation*

## Installations
* Clone the repository
    - `git clone <link-to-repo>`
* Change into the repo
    - `cd <path-to-repo>`

## Running the script
* One-time use
    - `python rename_files.py <dry-run-on|dry-run-off`
* Periodic use
    - Setup a cronjob `crontab -e`
    - Set script to run peridically (every monday, for example)
        + (from crontab) `* * * * mon python rename_files.py <dry-run-on|dry-run-off>`
*Running in dry-run-on mode allows you to view what would be renemaed without actually having the process take place. Try before you buy. Also: dry-run does not generate a log file.*

## Checking the Logs
The script creates a log file to display a few stats on what happened during the script run. This file lives at: `/tmp/file-renaming.log`

To display its contents, run `cat /tmp/file-renaming.log`