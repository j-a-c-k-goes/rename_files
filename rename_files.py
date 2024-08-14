'''
'''
import sys
import os
#---------------------------------------------------------------------------
def Msg(type, msg):
   print(f'[{type}]   {msg}')
#---------------------------------------------------------------------------
def Usage():
   print("[fix]     Specify whether or not to run the script in dry-run mode.")
   print("[usage]   <script-name> <dry-run-on|dry-run-off>")
   print("[example] rename_files.py dry-run-on\n")
#---------------------------------------------------------------------------
def CheckArgs():
   arg_check_passed = bool()
   if len(sys.argv) < 2:
      Msg('error', 'Not enough arguments.')
      arg_check_passed = False   
      Usage()
   else:
      Msg('update', 'Args present. Checking for correctness.')
      arg_to_check   = sys.argv[1]
      DRY_RUN_ON     = arg_to_check.lower() == 'dry-run-on'
      DRY_RUN_OFF    = arg_to_check.lower() == 'dry-run-off'
      valid_arg      = (DRY_RUN_ON) or (DRY_RUN_OFF)
      if valid_arg:
         arg_check_passed = True
         return { 'status': arg_check_passed, 'mode': arg_to_check }
      else:
         Msg('error', f'Invalid argument "{arg_to_check}".')
         arg_check_passed = False
         Usage()
   return { 'status': arg_check_passed, 'mode': None }
#---------------------------------------------------------------------------
def LookForNamingViolations(mode:str):
   files_in_naming_violation        = 0
   directories_in_naming_violation  = 0
   offending_directories            = list()
   offending_files                  = list()
   print(f'[mode] {mode}\n')
   print("Preparing to walk from home, '/'")
   try:
      for root, directories, files in os.walk('/', topdown=True, followlinks=True):
         for directory in directories:
            naming_violation = (' ' in directory)
            if naming_violation:
               directories_in_naming_violation += 1
               offending_directories.append(directory)
               prep_to_fix = directory.split()
               naming_fix  = '_'.join(prep_to_fix)      
               print(f'Renaming {root}/{directory} -> {root}/{naming_fix}')
               if (mode == 'dry-run-on'):
                  pass
               elif (mode =='dry-run-off'):
                  #os.system(f'mv {root}/{directory} -> {root}/{naming_fix}')
                  pass
         for file in files:
            naming_violation = (' ' in file)
            if naming_violation:
               files_in_naming_violation += 1
               offending_files.append(file)
               prep_to_fix = file.split()
               naming_fix  = '-'.join(prep_to_fix)
               print(f'Renaming {root}/{file} -> {root}/{naming_fix}')
               if (mode == 'dry-run-on'):
                  pass
               elif (mode =='dry-run-off'):
                  #os.system(f'mv {root}/{file} -> {root}/{naming_fix}')
                  pass
      return { 
         'naming_violations': 
         {
            'files': files_in_naming_violation, 
            'directories':  directories_in_naming_violation
         },
         'list_of_offenders': 
         {
            'files': offending_files,
            'directories': offending_directories
         }
      }
   except Exception as error:
      print(error)
      return -1
#---------------------------------------------------------------------------
# while open('/tmp/file-renaming.log', 'w') as source_file:
#    source_file.write('...')
#---------------------------------------------------------------------------
if __name__ == '__main__':
   arg = CheckArgs()
   try:
      if arg.get('status') == True:
         mode = arg.get('mode')
         Msg('update', 'Can proceed with checking for naming violations.')
         LookForNamingViolations(mode)
      else:
         exit(-1)
   except Exception as error:
      print(error)