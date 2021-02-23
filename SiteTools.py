import os
import re
import requests
from typing import List
from html.parser import HTMLParser

#import webbrowser webbrowser.open(link)



#######################################################################
#  Want to generate a list broken links on the entire site, together with their addresses
#######################################################################
# 1. Given a file system, want to expand directories recursively, returning a list of addresses
#   to each file
def expandDir(dir : List[str]) -> List[str]: # Wrapper function
    return sorted(__expandDir(dir), key=str.casefold)
def __expandDir(dir : List[str]) -> List[str]:
    for item in dir:            # checking each item in directory
        if os.path.isdir(item):     # if item is a directory, expand directory recursively
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



# 3. Create a mapping from <href> attributes to the files contining it { href : List of files containing href }
#   Adds <hrefs> attributes to a dict { href: isWorking } initialized to FALSE,

href_to_files_map = {}
href_IsWorking_map = {}
class HTML_Parser(HTMLParser):
    hrefs = set()
    def __init__(self, file : str, include = None):
        super().__init__()
        self.domain = re.compile("https?://(www\\.)?((?!nhn\\.ou.edu).)*$", re.IGNORECASE)
        self.file = file
        text = open(file, "r")
        self.feed(text.read()) # calls parse method on HTML file
        text.close()
    def handle_starttag(self, tag, attrs):
        if tag == "a":                                                       # filter <a > tags
            for attr in attrs:                                               # checking for <href> tag attributes
                if attr[0] == "href" and self.domain.match(attr[1]) != None: # excludes www.nhn.ou.edu/ <href> tags
                    if attr[1] in href_to_files_map.keys():
                        currentMapping = href_to_files_map[attr[1]]
                        currentMapping.append(self.file)
                        href_to_files_map[attr[1]] = sorted(currentMapping, key=str.casefold)  # adds to existing maps

                    else:
                        href_IsWorking_map[attr[1]] = None                  # creates new <href> -> boolean map
                        href_to_files_map[attr[1]] = [self.file]             # creates new <href> -> list of files containing <href> map
def scanHrefs(files : List[str], ignore = None):
    for file in files:
        HTML_Parser(file)

def get_href_IsWorking_map():
    return href_IsWorking_map
def get_href_to_files_map():
    return href_to_files_map
# 4. Confirm whether the hrefs are working

def confirmWorking():
    ct = 0
    for key in href_IsWorking_map.keys():
        if (ct % 20 == 0):
            print("Checked status of " + str(ct) + " unique external links")
            print("Progress : " + str(100*round(ct/len(href_IsWorking_map),2)) + "%")
        ct+=1
        try:
            r = requests.get(key, headers={
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})
            href_IsWorking_map[key] = str(r.history)+str(r.status_code)
        except:
            href_IsWorking_map[key] = "ERR"


# 5. Iterates through file_Hrefs_map, printing each file together with the broken resource
def printBrokenResources():
    pass
