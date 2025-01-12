import colorama
from colorama import Fore, Back, Style

colorama.init()

def PrintWarningLog(text):
    print(Fore.YELLOW + str(text))

def PrintInfoLog(text):
    print(Fore.GREEN + str(text))

def PrintErrorLog(text):
    print(Fore.RED + str(text))

def PrintDebugLog(text):
    print(Fore.LIGHTMAGENTA_EX + str(text))