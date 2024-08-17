import os
import sys

import logs

def CheckArgs():
   try:
      arg_check_passed = bool()
      if len(sys.argv) < 3:
         logs.Msg('error', 'Not enough arguments.')
         arg_check_passed = False   
         logs.Usage()
      else:
         logs.Msg('update', 'Args present. Checking for correctness.')
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
               logs.Msg('error', f'Invalid mode "{args_to_check[0]}".')
            if (valid_path == False):
               logs.Msg('error', f'Non-existing path "{args_to_check[1]}".')
            arg_check_passed = False
            logs.Usage()
      return { 'status': arg_check_passed, 'mode': None, 'path': None }
   except FileNotFoundError as exception:
      logs.Msg('exception', f'{sys.argv[2]} is not a vaild path')
      print(exception)
   except Exception as exception:
      logs.Msg('exception','See exception message.')
      print(exception)