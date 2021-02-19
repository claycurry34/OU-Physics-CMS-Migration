import os
from Physics.SiteTools import *


os.chdir("Physics/www.nhn.ou.edu")

items = os.listdir()
items = expandDir(items)    # 1. gets path of all files

#items = filterHTML(["assets/alum-photos/friedman-bike.jpg"])
items = filterHTML(items)   # 2. reads each of 1. and removes nonhtml
print(items)