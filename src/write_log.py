''' IMPORTS '''
import sys
import times
from msg import Msg

''' ROUTINE/METHOD '''
def WriteLog(file_name:str, mode:str, log_statements:list):
   '''
      @method WriteLog
      @param file_name:string    # repesents output file
      @param mode:string         # represents mode program is running in
      @param log_statements:list # represents list of log statements to write
      @return void
      @desc Method attempts to log the session to an output file. 
   '''
   try:
      with open(file_name, 'w') as source_file:
         year     = times.year
         month    = times.month
         day      = times.month
         hour     = times.hour
         minute   = times.minute
         source_file.write('---\n')
         source_file.write(f'TIMESTAMP {year}/{month}/{day} @ {hour}:{minute}\n')
         source_file.write(f'ran {sys.argv[0]} in {mode} mode\n'.upper())
         source_file.write('---\n')
         if len(log_statements) < 1:
            source_file.write('No log statements to report.\n')
         if (mode == 'dry-run-on'):
            source_file.write('There is no logging when DRY-RUN-ON\n')
         else:
            for index, log_statement in enumerate(log_statements):
               source_file.write(f'[{index}]    {log_statement}\n')
         print(f'Done writing {file_name}.')
   except FileNotFoundError as fnf_exception:
      Msg('action', f'{file_name} not found. Check path or spelling.')
      Msg('exception', fnf_exception)
   except Exception as general_exception:
      Msg('action', 'Consult error message below for details.')
      Msg('exception', general_exception)
