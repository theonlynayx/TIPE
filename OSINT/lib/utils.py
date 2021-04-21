from bs4 import BeautifulSoup as bs
from collections import OrderedDict
from OSINT.lib.colors import *
from OSINT.config import *
from PIL import Image
from time import sleep
import itertools
import requests
import sys
import os

# 𝑭𝒊𝒏𝒅 𝑯𝒂𝒔𝒉𝑻𝒂𝒈𝒔 𝒂𝒏𝒅 𝒕𝒂𝒈𝒈𝒆𝒅 𝒖𝒔𝒆𝒓𝒔 𝒊𝒏 𝒄𝒂𝒑𝒕𝒊𝒐𝒏

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
            f.close()
            return False

# 𝑺𝒐𝒓𝒕 𝒍𝒊𝒔𝒕 𝒃𝒚 𝒇𝒓𝒆𝒒𝒖𝒆𝒏𝒄𝒚 𝒂𝒏𝒅 𝒓𝒆𝒎𝒐𝒗𝒆 𝒅𝒖𝒑𝒍𝒊𝒄𝒂𝒕𝒆

def sorting(ListToSort):
    ListSorted = sorted(ListToSort, key = ListToSort.count,reverse = True) 
    ListSorted = list(OrderedDict.fromkeys(ListSorted))
    return ListSorted

def fail(message):
    print(f"{FAIL}{message}{END}")
    os._exit(1)

# Fonction à remplacer par un logo de chargement si Sacha se dépêche héhé ^^

def loading(waiter):
    while waiter.isSet() == False:
        print("WAIT")
        sleep(2)
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
    return "Profiles/" + FolderName

    
def InsertLines(filename,index,text):
    with open(filename,"rb") as f:
        a = f.readlines()
        f.close()
    a.insert(index,(text + "\n").encode('UTF-8'))

    with open(filename,"wb") as f:
        f.write(b"".join(a))
        f.close()

def convertImg(path):
    img = Image.open(path)
    img.save(path.replace('.jpg','.png'))
