''' program main.py -- automates renaming of files containing a specific delimiter '''

''' IMPORTS '''
from cli import CheckArgs
from rename_files import LookForNamingViolations
from msg import Msg

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
