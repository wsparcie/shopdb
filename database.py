from os import system
from time import sleep
from glob import iglob
from datetime import datetime

from preferences import*
from user import User
from product import Product
from order import Order
from review import Review
from login import Login

class Database:
    def __init__(self):
        self.R = React()
        self.dirType = (
            'preferences.txt',
            'login.txt',
            'users.txt',
            'products.txt',
            'orders.txt',
            'reviews.txt',
        )

        self.menuType = {
            'us': 'users',
            'pd': 'products',
            'ord': 'orders',
            'rev': 'reviews',
            'sv': 'save',
            'ex': 'exit',
            'clear': 'clear',
        }

        self.menuNonUsable = (
            'sv',
            'ex',
            'clear',
        )
    
        self.funcsType = {
            'ls': 'list',
            'sr': 'sort',
            'fl': 'filter',
            'add': 'add',
            'del': 'delete',
            'mdf': 'modify',
            'sv': 'save',
            'ex': 'exit',
        }

        self.login = Login()
        self.users = User()
        self.products = Product()
        self.orders = Order(self.users, self.products)
        self.reviews = Review(self.users, self.products)
        self.ifIntegral = self.__checkFiles()

        if self.ifIntegral:
            print(f"{self.R.warnSplitL} reading database {self.R.warnSplitR}")
            for key, value in self.menuType.items():
                if key not in self.menuNonUsable:
                    getattr(self, value).read()
            self.login.signIn()
            self.name = self.prefLoad()
        else:
            print(f"{self.R.warnSplitL} generating database {self.R.warnSplitR}")
            for key, value in self.menuType.items():
                if key not in self.menuNonUsable:
                    getattr(self, value).generate()
            self.login.signUp()
            self.name = self.prefSave()

    def __checkFiles(self):
        try:
            print(f"{self.R.warnSplitL} {'checking files'} {self.R.warnSplitR}")
            directory = [file for file in iglob("*.txt") if file != 'requirements.txt']
            files = set([*self.dirType, *directory])
            isComplete = len(files) == len(directory)
            if len(directory) != 0 and not isComplete:
                self.R.printIncorrectItem('missing files')
            return isComplete
        except Exception as e:
            self.R.printException('checking files', e)
            return 0

    def prefSave(self):
        try:
            text = 'Please enter service name: '
            name = input(text).strip()
            with open('preferences.txt', 'w') as file:
                file.write(name)
            text = 'name saved'
            print(f'{self.R.reSplitL} {text} {self.R.reSplitR}')
            sleep(1)
            return name
        except Exception as e:
            self.R.printException('saving preferences', e)

    def prefLoad(self):
        try:
            with open('preferences.txt', 'r') as file:
                name = file.readline().strip()
            return name
        except Exception as e:
            self.R.printException('loading preferences', e)

    def info(self):
        print(self.R.header)
        text = f'Welcome back to {self.name}'
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tabs = ' '*(len(self.R.header)//8-len(text))
        text1 = f'{bcolors.OKGREEN}{text}'
        text2 = f'{tabs}{time}{bcolors.ENDC}'
        welcome = f'{text1}{text2}'
        print(welcome, end = '\n\n')
        text = 'STATS:'
        print(f'{bcolors.BOLD}{text}{bcolors.ENDC}', end = '\t')
        status = ' | '.join(f'{self.dataVolume(key)} {value}'
                        for key, value in self.menuType.items() 
                        if key not in self.menuNonUsable)
        print(status, end = '\n\n')

    def dataVolume(self, name):
        if name not in self.menuNonUsable:
            attr = self.menuType[name]
            return getattr(self, attr).volume()

    def saveData(self, selection):
        if selection == 'all':
            for key, value in self.menuType.items():
                if key not in self.menuNonUsable:
                    getattr(self, value).save()
            print(f'{self.R.warnSplitL} saving database {self.R.warnSplitR}')
            sleep(1)
        else:
            name = self.menuType[selection]
            getattr(self, name).save()
            print(f'\t{self.R.warnSplitL} saving {name} {self.R.warnSplitR}')
            sleep(1)
    
    def __exited(self, tabs):
        text = 'exiting'
        text1 = f'{'\t'*tabs}{bcolors.FAIL}{self.R.warnSplitL}'
        text2 = f'{text} {self.R.warnSplitR}'
        print(f'{text1} {text2}')
        sleep(1)
        return 1

    def __failed(self, tabs):
        text = 'incorrect selection'
        text1 = f'{bcolors.FAIL}{'\t'*tabs}'
        text2 = f'{self.R.warnSplitL} {text} {self.R.warnSplitR}'
        print(f'{text1} {text2}')
        sleep(1)
        return 0
    
    def __exSelect(self):
        text = 'SAVE data? [y/n]: '
        text = f'{bcolors.WARNING}{text}{bcolors.ENDC}'
        ifSave = input(text).strip().lower()
        if ifSave == 'y':
            self.saveData('all')

    def __home(self):
        print(f'{self.R.splitL} PLEASE SELECT {self.R.splitR}')
        [print(f'{key}. {value}', end = ' | ') 
         for key, value in self.menuType.items()]
        text = 'YOUR SELECTION >>> '
        text = f'{bcolors.HEADER}{text}{bcolors.ENDC}'
        selection = input(text)
        selection = selection.strip().lower()
        if selection == 'sv':
            self.saveData('Fall')
            return 0
        elif selection == 'ex':
            self.__exSelect()
            return self.__exited(0)
        elif selection == 'clear':
            system('cls||clear')
            self.info()
            return 0
        elif selection in self.menuType:
            attr = self.menuType[selection]
            self.homeSel = getattr(self, attr)
        else:
            return self.__failed(0)
        return selection
    
    def __delSel(self, selection):
        if selection == 'us':
            id = self.users.delete()
            if id not in (-1, 0):
                self.orders.delByUserID(id)
                self.reviews.delByUserID(id)
        elif selection == 'pd':
            id = self.products.delete()
            if id not in (-1, 0):
                self.reviews.delByProductID(id)
        else:
            getattr(self.homeSel, 'delete')()

    def __subHome(self, selectionHome):
        section = self.menuType[selectionHome].upper()
        print(f'\t{self.R.splitL} {section} section {self.R.splitR}', end = '\n\t')
        [print(f'{key}. {value}', end = ' | ') 
         for key, value in self.funcsType.items()]
        text = 'YOUR REQUEST >>> '
        text = f'{bcolors.HEADER}{text}{bcolors.ENDC}'
        selection = input(text)
        selection = selection.strip().lower()
        if selection == 'sv':
            self.saveData(selectionHome)
        elif selection == 'ex':
            return self.__exited(1)
        elif selection == 'del':
            self.__delSel(selectionHome)
        elif selection in self.funcsType:
            attr = self.funcsType[selection]
            getattr(self.homeSel, attr)()
        else:
            return self.__failed(1)
        return selection

    def menu(self):
        try:
            self.info()
            while True:
                status = self.__home()
                if status == 1:
                    break
                elif status != 0:
                    while True:
                        s = self.__subHome(status)
                        if s == 1:
                            break
        except Exception as e:
            self.R.printException('main menu', e)
        return -1