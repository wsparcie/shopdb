
import bcrypt
from getpass import getpass

from preferences import*

class Login:
    def __init__(self):
        self.R = React()
    
    def signUp(self):
        try:
            print(f'{self.R.splitL} SIGN UP {self.R.splitR}')
            print('Please setup your login info: ')
            hashed = bcrypt.hashpw(
                getpass('login: ').strip().encode('utf-8'),
                bcrypt.gensalt())
            with open('login.txt', 'wb') as loginFile:
                loginFile.write(hashed)
            text = f'login saved'
            print(f'{self.R.reSplitL} {text} {self.R.reSplitR}')
            return 1
        except Exception as e:
            self.R.printException('signing up', e)
            return 0

    def signIn(self):
        try:
            print(f'{self.R.splitL} SIGN IN {self.R.splitR}')
            print('Please pass your login info: ')
            while True:
                def checkLogin():
                    with open('login.txt', 'rb') as loginFile:
                        hashed = loginFile.readline()
                    ifPassed = bcrypt.checkpw(
                        getpass('login: ').strip().encode('utf-8'),
                        hashed)
                    return ifPassed
                ifPassed = checkLogin()
                if ifPassed:
                    text = 'SIGNED IN'
                    print(f'{self.R.reSplitL} {text} {self.R.reSplitR}')
                    return 1
                else:
                    text = 'incorrect info'
                    print(f'{self.R.failSplitL} {text} {self.R.failSplitR}')
        except Exception as e:
            self.R.printException('signing in', e)
            return 0