import sys

import times


# -------------------------------------------------------------------------
def Usage():
   print(f'[fix]        Specify whether or not to run the script in dry-run mode.')
   print(f'[usage]      <script-name> <dry-run-on|dry-run-off> <some-path>')
   print(f'[example]    rename_files.py dry-run-on /home\n')
   
#---------------------------------------------------------------------------
def Msg(type, msg):
   print(f'[{type}]    {msg}')

#---------------------------------------------------------------------------
def WriteLog(file_name, mode, log_statements:list):
   try:
      with open(file_name, 'w') as source_file:
         source_file.write('---\n')
         source_file.write(f'TIMESTAMP {times.year}/{times.month}/{times.day} @ {times.hour}:{times.minute}\n')
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
      Msg('exception', 'Consult error message below for details.')
      print(general_exception)