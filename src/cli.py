''' IMPORTS '''
import os
import sys
from write_log import WriteLog
from msg import Msg
from usage import Usage

''' METHOD/ROUTINE '''
def CheckArgs() -> dict:
   '''
      @method CheckArgs
      @param void
      @return dict {status, mode, path}
      @desc Checks command line args. Returns a dictionary.
   '''
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
               pass
               Msg('error', f'Invalid mode {args_to_check[0].upper()}')
            if (valid_path == False):
               pass
               Msg('error', f'Non-existing path {args_to_check[1].upper()}')
            arg_check_passed = False
            Usage()
      return { 'status': arg_check_passed, 'mode': None, 'path': None }
   except FileNotFoundError as exception:
      Msg('update', f'{sys.argv[2]} is not a vaild path')
      Msg('exception', exception)
   except Exception as exception:
      Msg('exception', exception)
