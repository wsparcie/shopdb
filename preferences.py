from time import sleep
from colorama import Fore

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    OKLEMON = '\033[90m'
    OKLIME = '\033[89m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class React:
    def __init__(self):
        splitL = r'\________'
        splitR = r'_________'
        reSplitL = r'---------'
        reSplitR = r'---------'
        failSplitL = r'!!!!!!!!!'
        failSplitR = r'!!!!!!!!!'
        warnSplitL = r'>>>>>>>>>'
        warnSplitR = r'<<<<<<<<<'

        self.splitL = f'{bcolors.HEADER}{splitL}'
        self.splitR = f'{splitR}{bcolors.ENDC}'
        self.reSplitL = f'{bcolors.OKGREEN}{reSplitL}'
        self.reSplitR = f'{reSplitR}{bcolors.ENDC}'
        self.failSplitL = f'{bcolors.FAIL}{failSplitL}'
        self.failSplitR = f'{failSplitR}{bcolors.ENDC}'
        self.warnSplitL = f'{bcolors.WARNING}{warnSplitL}'
        self.warnSplitR = f'{warnSplitR}{bcolors.ENDC}'

    def printException(self, name, e):
        text = 'error while'
        infoText = f'{self.failSplitL} {text} {name} {self.failSplitR}'
        errorText = f'{self.warnSplitL}{e}{self.warnSplitR}'
        print(f'\t\t{infoText}\n{errorText}')
        sleep(1)

    def printFileNotFound(self, name):
        print(f'\t\t{self.failSplitL} {name} not found {self.failSplitR}')
        sleep(1)

    def printIncorrectItem(self, name):
        print(f'\t\t{self.failSplitL} incorrect {name} {self.failSplitR}')
        sleep(1)

    def printActionTaken(self, name):
        print(f'\t\t{self.reSplitL} {name.upper()} {self.reSplitR}')
        sleep(1)

    def printTakeAction(self, name):
        text = f'\t\t{name} [y/n]: '
        status = input(f'{bcolors.WARNING}{text}{bcolors.ENDC}')
        status = status.strip().lower()
        return status

    def printRequest(self, name):
        print(f'\t\t{self.splitL} {name.upper()} request {self.splitR}')

    def printSection(self, name):
        print(f'\t\t{self.splitL} {name.upper()} section {self.splitR}')

    def exited(self, tabs):
        text = 'exiting'
        print(f'{'\t'*tabs}{bcolors.FAIL}{self.warnSplitL} {text} {self.warnSplitR}')
        sleep(1)
        return 1

    def failed(self, tabs):
        text = 'incorrect selection'
        print(f'{bcolors.FAIL}{'\t'*tabs}{self.warnSplitL} {text} {self.warnSplitR}')
        sleep(1)
        return 0

    l = f'{Fore.BLUE}'
    r = f'{Fore.WHITE}'
    header = f"""
{r}
{l}        ███████╗██╗  ██╗ ██████╗ ██████╗ ██████╗  █████╗ ████████╗ █████╗ ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
{l}        ██╔════╝██║  ██║██╔═══██╗██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
{l}        ███████╗███████║██║   ██║██████╔╝██║  ██║███████║   ██║   ███████║██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
{l}        ╚════██║██╔══██║██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══██║██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
{l}        ███████║██║  ██║╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ██║  ██║██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
{l}        ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
{r}                                                                                                                            
    """

nUsers = 75
nProducts = 100
nOrders = 50
nReviews = 25