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
def expandFilePaths(dir : List[str]) -> List[str]: # Wrapper function
    return sorted(__expandFilePaths(dir), key=str.casefold)
def __expandFilePaths(dir : List[str]) -> List[str]:
    for item in dir:            # checking each item in directory
        if os.path.isdir(item):     # if item is a directory, expand directory recursively
            os.chdir(item)
            subdir = os.listdir()
            files = [item + "/" + s for s in expandFilePaths(subdir)]
            dir.remove(item)
            dir = dir + files
            os.chdir("..")
    return dir



# 2. Filter for only HTML files from the list from (1.), by reading contents of file
def filterHTML(files, exclude = ".*?\\.(js|jpg|pdf)"): #-> List[bool]:
    parse = re.compile("(\\r?\\n)*?<!\\s*?DOCTYPE\\s+?html", re.IGNORECASE)
    skip = re.compile(exclude)
    size = len(files)
    i = 0
    ct = 0
    for i in range(len(files)-1,0,-1):
        if (ct % 100 == 0):
            print("Filtered " + str(ct) + " files--Progress : " + str(int(1000*ct/size)/10) + "%")
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
    print("\nCompleted filtering of " + ct.__str__() + " files.\nDiscovered " + len(files).__str__() + " html files\n")
    return files



# 3. Create a mapping from <href> attributes to the files contining it { href : List of files containing href }
#   Adds <hrefs> attributes to a dict { href: isWorking } initialized to FALSE,

href_to_files_map = {}
file_to_hrefs_map = {}
href_IsWorking_map = {}
class HTML_Parser(HTMLParser):
    hrefs = set()
    def __init__(self, file : str, include = None):
        super().__init__()
        self.domain = re.compile("https?://(www\\.)?((?!nhn\\.ou.edu).)*$", re.IGNORECASE)
        self.file = file
        file_to_hrefs_map[file] = [] # creates a <file> -> href : List
        text = open(file, "r")
        self.feed(text.read()) # calls parse method on HTML file
        text.close()
    def handle_starttag(self, tag, attrs):
        if tag == "a":                                                       # filter <a > tags
            for attr in attrs:                                               # checking for <href> tag attributes
                if attr[0] == "href" and self.domain.match(attr[1]) != None: # excludes www.nhn.ou.edu/ <href> tags
                    if not attr[1] in file_to_hrefs_map[self.file]:          # populates files_to_hrefM
                        file_to_hrefs_map[self.file].append(attr[1])
                    if attr[1] in href_to_files_map.keys():
                        currentMapping = href_to_files_map[attr[1]]
                        currentMapping.append(self.file)
                        href_to_files_map[attr[1]] = sorted(currentMapping, key=str.casefold)  # adds to existing maps

                    else:
                        href_IsWorking_map[attr[1]] = None                  # creates new <href> -> boolean map
                        href_to_files_map[attr[1]] = [self.file]             # creates new <href> -> list of files containing <href> map
def build_href_maps(files : List[str], ignore = None):
    print("building href maps")
    for file in files:
        HTML_Parser(file)

def get_href_IsWorking_map():
    return href_IsWorking_map
def get_href_to_files_map():
    return href_to_files_map
def get_file_to_hrefs_map():
    return file_to_hrefs_map
# 4. Confirm whether the hrefs are working


def stringify_http_redirect_history(http_redirect_history : List[str])->str:
    response_code = re.compile("\\d+") # detects number in HTTP response
    history = ""
    if len(http_redirect_history) > 0:
        for response in http_redirect_history:
            try:
                code = response_code.search(str(response))
                history += code.group(0) + "->"
            except:
                pass
    return history



def get_site_status(href_item : str):
    # Perform HTTP request (print -1 for exception)
    try:
        r = requests.get(href_item, headers={
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"})
        href_IsWorking_map[href_item] = r.status_code, r.history  # Assign HTTP response to isWorking map
    except:  # Assign HTTP response to isWorking map
        href_IsWorking_map[href_item] = -1, [""]  # Assign -1 as HTTP response to isWorking map if error occurs


def print_status_by_site():
    print("\n Checking site status codes")
    ct = 0
    sitesChecked = 0
    print("file, href, status history, exit status", file=open("hrefs.csv", "w")) # initialize top line of CSV file
    for file in file_to_hrefs_map:
        for href_item in file_to_hrefs_map[file]:
            if href_IsWorking_map[href_item] == None:
                get_site_status(href_item)
                # Progress indicator
                sitesChecked += 1
                if (sitesChecked % 5 == 0):  # Progress indicator
                    print("Checked status of " + str(sitesChecked) + " external links")  # Progress indicator
                    print("Progress : " + str(
                        round(100 * sitesChecked / len(href_IsWorking_map), 3)) + "%")  # Progress indicator

            (http_exit_number, history) = href_IsWorking_map.get(href_item)
            history = stringify_http_redirect_history(history)

            print(file + ", " + href_item + ", " + history + ", " + str(http_exit_number), file=open("hrefs.csv", "a"))
    return
def stringify_sites(href_item : str):
    response = ""
    for site in href_to_files_map:
        response = site + "; "
    return response.rstrip(" ;")


# 5. Iterates through file_Hrefs_map, printing each file together with the broken resource
def print_status_by_href():
    print("href, status history, exit status", file=open("status_by_href.csv", "w")) # initialize top line of CSV file
    for href_item in href_IsWorking_map:
        if href_IsWorking_map[href_item] == None:
            get_site_status(href_item)

        (http_exit_number, history) = href_IsWorking_map.get(href_item)
        history = stringify_http_redirect_history(history)
        sites = stringify_sites(href_item)
        print(href_item + ", " + history + ", " + str(http_exit_number) + ", " + sites, file=open("status_by_href.csv", "a"))
