''' IMPORTS '''
import os
from write_log import WriteLog
import times
from msg import Msg

def LookForNamingViolations(path, mode:str):
   try:
      delimiter                        = ' '
      file_replacement_char            = '-'
      dir_replacement_char             = '_'
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
               evaluation_directory = directory
               naming_violation     = (' ' in evaluation_directory)
               if naming_violation:
                  directories_in_naming_violation += 1
                  prep_to_fix          = evaluation_directory.split(delimiter)
                  naming_fix           = dir_replacement_char.join(prep_to_fix)
                  evaluation_directory = naming_fix      
                  log_statement        = f'Renamed {root}/{directory} -> {root}/{evaluation_directory}'
                  if (mode == 'dry-run-on'):
                     Msg('msg', log_statement)
                  elif (mode =='dry-run-off'):
                     tmp_log_statements_dirs.append(log_statement)
                     command_to_run = f'mv "{root}/{directory}" {root}/{naming_fix}'
                     os.system(command_to_run)
            for file in files:
               evaluation_file = file
               naming_violation = (' ' in evaluation_file)
               if naming_violation:
                  files_in_naming_violation += 1
                  prep_to_fix     = evaluation_file.split()
                  naming_fix      = file_replacement_char.join(prep_to_fix)
                  evaluation_file = naming_fix
                  log_statement   = f'Renamed {root}/{file} -> {root}{evaluation_file}'
                  if (mode == 'dry-run-on'):
                     Msg('msg', log_statement)
                  elif (mode =='dry-run-off'):
                     command_to_run = f'mv "{root}/{file}" {root}/{evaluation_file}'
                     os.system(command_to_run)
                     tmp_log_statements_files.append(log_statement)
         year     = times.year
         month    = times.month
         day      = times.month
         hour     = times.hour
         minute   = times.minute
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