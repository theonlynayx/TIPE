from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from OSINT.lib.colors import *
from OSINT.config import *
from time import sleep
import itertools
import requests
import sys
import os

def MakeAChoice(string):
    while True:
        sys.stdout.write(f"{HEADER}[?] {string} [Y/N]{END}")
        sys.stdout.flush()
        inpt = sys.stdin.readline()
        if inpt.replace("\n","") == "Y":
            sys.stdout.write(StrClear.replace("\n",""))
            return True
        elif inpt.replace("\n","") == "N":
            sys.stdout.write(StrClear.replace("\n",""))
            return False
        sys.stdout.write(StrClear.replace("\n",""))

# Find HashTags and tagged users in caption

def ExtractThroughCaption(Finder,caption):
    ResultList = []
    TagList = ""
    IterCaption = iter(caption)
    while True:
        try:
            char = next(IterCaption)
            if char == Finder:
                while char != " ":
                    char = next(IterCaption)
                    TagList += char
        except StopIteration:
            ResultList.append(TagList.split())
            break
    return TagList.split()

def GetPicsAndVid(url,filename):
    with open(filename,"wb") as f:
        try:
            r = requests.get(str(url),headers=headers)
            f.write(r.content)
            f.close()
            return True
        except:
            return False

# Sort list by frequency and remove duplicate

def sorting(ListToSort):
    ListSorted = sorted(ListToSort, key = ListToSort.count,reverse = True) 
    ListSorted = list(OrderedDict.fromkeys(ListSorted))
    return ListSorted

def fail(message):
    print(StrClear)
    print(f"{FAIL}{message}{END}")
    os._exit(1)

# animation pimp af

def loading(waiter,color,WaitingString):

    ClockList = ["\U0001F55B","\U0001F550","\U0001F551","\U0001F552","\U0001F553","\U0001F554",
                    "\U0001F555","\U0001F556","\U0001F557","\U0001F558","\U0001F559","\U0001F55a"]

    sys.stdout.write(color + f"[*] {WaitingString}: ")
    sys.stdout.flush()
    ClockCycle = itertools.cycle(ClockList)
    while waiter.isSet() == False:
        sys.stdout.write('\b' * 2)
        sys.stdout.write(next(ClockCycle))
        sys.stdout.flush()
        sleep(0.05)
    sys.stdout.write(END)
    sys.exit()

def CreateFolder(UserName):

    n = 1
    FolderName = UserName

    while os.path.exists("Profiles\\{}".format(FolderName)) is True:
        FolderName = UserName + "_" + str(n)
        n += 1
    
    os.chdir("Profiles")
    os.mkdir(FolderName)
    os.chdir(FolderName)

    
def InsertLines(filename,index,text):
    with open(filename,"rb") as f:
        a = f.readlines()
        f.close()
    a.insert(index,(text + "\n").encode('UTF-8'))

    with open(filename,"wb") as f:
        f.write(b"".join(a))
        f.close()
    
