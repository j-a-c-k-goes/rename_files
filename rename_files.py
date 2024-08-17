'''
    Program: rename_files.py
    
    Objective: automate renaming of files named with delimiter space
    
    Design:
    
    Test:         run in test environment, 
                  (from test env) run with dry-run-off
    
    Modification: target more delimiters
'''
import os

import cli
import logs
import times

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
         logs.Msg('error', f'Cannot walk non-existing path ({path})')
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
         logs.WriteLog(f'/tmp/{times.year}{times.month}{times.day}{times.hour}{times.minute}-log-files-renamed.log', mode, tmp_log_statements_files)
         logs.WriteLog(f'/tmp/{times.year}{times.month}{times.day}{times.hour}{times.minute}-log-directories-renamed.log', mode, tmp_log_statements_dirs)
         logs.Msg('files-renamed', files_in_naming_violation)
         logs.Msg('directories-renamed', directories_in_naming_violation)
         logs.Msg('total', (files_in_naming_violation+directories_in_naming_violation))
   except KeyboardInterrupt as exception:   
         logs.Msg('action', 'process stopped intentionally. writing log up to this point') 
         logs.Msg('exception', exception)
   except Exception as exception:
         logs.Msg('action', 'non-interrupt has halted process.')      
         logs.Msg('exception', exception)
         return -1
   
#---------------------------------------------------------------------------
if __name__ == '__main__':
   arg = cli.CheckArgs()
   try:
      if arg.get('status') == True:
         path_to_walk = arg.get('path')
         mode = arg.get('mode')
         logs.Msg('update', 'Can proceed with checking for naming violations.')
         LookForNamingViolations(path_to_walk, mode)
      else:
         exit(-1)
   except Exception as error:
      print(error)
