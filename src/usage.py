''''''
def Usage():
   '''
      @method Usage
      @param void
      @return void
      @desc Prints script usage tips, examples.
   '''
   print(f'[fix]        Specify whether or not to run the script in dry-run mode.')
   print(f'[usage]      <script-name> <dry-run-on|dry-run-off> <some-path>')
   print(f'[example]    rename_files.py dry-run-on /home\n')