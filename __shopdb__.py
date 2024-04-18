print('please wait...')

import subprocess
import sys
from os import system
from time import sleep

from login import Login
from database import Database

try:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    import bcrypt
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'colorama'])
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'bcrypt'])
    print('installing modules')
finally:
    from colorama import just_fix_windows_console
    just_fix_windows_console()
    import bcrypt
    print('importing modules')

class Main(Database):
    def __init__(self):
        self.base = Database()

    def main(self):
        sleep(2)
        system('cls||clear')
        self.base.menu()

if __name__ == '__main__':
    Main().main()