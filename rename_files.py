'''
    Program: rename_files.py
    
    Objective: automate renaming of files named with delimiter space
    
    Design:
    
    Test:         run in test environment, 
                  (from test env) run with dry-run-off
    
    Modification: target more delimiters
'''
import sys
import os
import datetime
#---------------------------------------------------------------------------
month    = datetime.datetime.now().month
year     = datetime.datetime.now().year
day      = datetime.datetime.now().day
hour     = datetime.datetime.now().hour
minute   = datetime.datetime.now().minute
#---------------------------------------------------------------------------
def Msg(type, msg):
   print(f'[{type}]    {msg}')
#---------------------------------------------------------------------------
def Usage():
   print(f'[fix]        Specify whether or not to run the script in dry-run mode.')
   print(f'[usage]      <script-name> <dry-run-on|dry-run-off> <some-path>')
   print(f'[example]    rename_files.py dry-run-on /home\n')
#---------------------------------------------------------------------------
def CheckArgs():
   try:
      arg_check_passed = bool()
      if len(sys.argv) < 3:
         Msg('error', 'Not enough arguments.')
         arg_check_passed = False   
         Usage()
      else:
         Msg('update', 'Args present. Checking for correctness.')
         args_to_check  = [ sys.argv[1], sys.argv[2] ]
         DRY_RUN_ON     = args_to_check[0].lower() == 'dry-run-on'
         DRY_RUN_OFF    = args_to_check[0].lower() == 'dry-run-off'
         valid_mode     = (DRY_RUN_ON) or (DRY_RUN_OFF)
         valid_path     = os.path.exists(args_to_check[1])
         if (valid_mode and valid_path):
            arg_check_passed = True
            return { 'status': arg_check_passed, 'mode': args_to_check[0], 'path': args_to_check[1] }
         else:
            if (valid_mode == False):
               Msg('error', f'Invalid mode "{args_to_check[0]}".')
            if (valid_path == False):
               Msg('error', f'Non-existing path "{args_to_check[1]}".')
            arg_check_passed = False
            Usage()
      return { 'status': arg_check_passed, 'mode': None, 'path': None }
   except FileNotFoundError as exception:
      Msg('exception', f'{sys.argv[2]} is not a vaild path')
      print(exception)
   except Exception as exception:
      Msg('exception','See exception message.')
      print(exception)
#---------------------------------------------------------------------------
def LookForNamingViolations(path, mode:str):
   try:
      files_in_naming_violation        = 0
      directories_in_naming_violation  = 0
      tmp_log_statements_files         = list()
      tmp_log_statements_dirs          = list()
      log_statements                   = { 'files': list(), 'directories': list() }
      print(f'[mode] {mode}\n')
      if (not os.path.exists(path)):
         Msg('error', f'Cannot walk non-existing path ({path})')
         exit(-1)
      else:
         print(f'Preparing to walk from "{path}"')
         for root, directories, files in os.walk(f'{path}', topdown=True, followlinks=True):
            for directory in directories:
               naming_violation = (' ' in directory)
               if naming_violation:
                  directories_in_naming_violation += 1
                  prep_to_fix    = directory.split()
                  naming_fix     = '_'.join(prep_to_fix)      
                  log_statement  = (f'Renamed {root}/{directory} -> {root}/{naming_fix}')
                  if (mode == 'dry-run-on'):
                     print(log_statement)
                  elif (mode =='dry-run-off'):
                     os.system(f'mv {root}/{directory} -> {root}/{naming_fix}')
                     tmp_log_statements_dirs.append(log_statement)
            for file in files:
               naming_violation = (' ' in file)
               if naming_violation:
                  files_in_naming_violation += 1
                  prep_to_fix    = file.split()
                  naming_fix     = '-'.join(prep_to_fix)
                  log_statement  = (f'Renamed {root}/{file} -> {root}/{naming_fix}')
                  if (mode == 'dry-run-on'):
                     print(log_statement)
                  elif (mode =='dry-run-off'):
                     os.system(f'mv {root}/{file} -> {root}/{naming_fix}')
                     tmp_log_statements_files.append(log_statement)
                     pass
         WriteLog(f'/tmp/{year}{month}{day}{hour}{minute}-log-files-renamed.log', mode, tmp_log_statements_files)
         WriteLog(f'/tmp/{year}{month}{day}{hour}{minute}-log-directories-renamed.log', mode, tmp_log_statements_dirs)
         Msg('files-renamed', files_in_naming_violation)
         Msg('directories-renamed', directories_in_naming_violation)
         Msg('total', (files_in_naming_violation+directories_in_naming_violation))
   except KeyboardInterrupt as exception:   
         Msg('action', 'process stopped intentionally. writing log up to this point') 
         Msg('exception', exception)
   except Exception as exception:
         Msg('action', 'non-interrupt has halted process.')      
         Msg('exception', exception)
         return -1
#---------------------------------------------------------------------------
def WriteLog(file_name, mode, log_statements:list):
   try:
      with open(file_name, 'w') as source_file:
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
      Msg('exception', 'Consult error message below for details.')
      print(general_exception)
#---------------------------------------------------------------------------
if __name__ == '__main__':
   arg = CheckArgs()
   try:
      if arg.get('status') == True:
         path_to_walk = arg.get('path')
         mode = arg.get('mode')
         Msg('update', 'Can proceed with checking for naming violations.')
         LookForNamingViolations(path_to_walk, mode)
      else:
         exit(-1)
   except Exception as error:
      print(error)
