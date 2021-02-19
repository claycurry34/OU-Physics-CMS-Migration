import os
import re
from typing import List


#for item in items:
#   isDir = "directory" if os.path.isdir(item) else "file"
#    print("" + item + " is a " + isDir)

#######################################################################
#  Make a list broken links, together with their addresses
#######################################################################
# 1. Given a file system, want to expand directories recursively, returning a list of addresses
#   to each file
def expandDir(dir : List[str]) -> List[str]:
    return sorted(__expandDir(dir), key=str.casefold)

def __expandDir(dir : List[str]) -> List[str]:
    for item in dir:            # checking each item in directory
        if os.path.isdir(item):     # if some item is a directory,
            os.chdir(item)
            subdir = os.listdir()
            files = [item + "/" + s for s in expandDir(subdir)]
            dir.remove(item)
            dir = dir + files
            os.chdir("..")
    return dir



# 2. Filter for only HTML files from the list from (1.), by reading contents of file
def filterHTML(files, exclude = ".*?\\.(js|jpg|pdf)"): #-> List[bool]:
    parse = re.compile("(\\r?\\n)*?<!\\s*?DOCTYPE\\s+?html", re.IGNORECASE)
    skip = re.compile(exclude)
    i = 0
    ct = 0
    for i in range(len(files)-1,0,-1):
        if (ct % 100 == 0):
            print("Parsed " + str(ct) + " files")
        ct+=1
        response = None
        try:
            if (skip.match(files[i]) != None):
                raise AttributeError
            f = open(files[i], "r")
            response = parse.match(f.read())
            f.close()
        except:
            pass
        if(response == None):
            del files[i]


    return files


# 3. Adds HTML files to a dict mapping to list of <href> attributes { File: List of hrefs }
#   Adds <hrefs> attributes to a dict { href: isWorking } initialized to FALSE,

def generateDicts():

    file_Hrefs_map = {}
    href_isWorking_map = {}

# 4. Confirm whether the hrefs are working

# 5. Iterates through file_Hrefs_map, printing each file together with the broken resource
def printBrokenResources():
    pass