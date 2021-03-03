import os
from SiteTools import *
#from Physics.SiteTools import expandDir, filterHTML


os.chdir("www.nhn.ou.edu")
items = expandDir(os.listdir())    # 1. gets path of all files
items = filterHTML(items)          # 2. reads each file to determine HTML

build_href_maps(items, ignore="(@|/|https://www.nhn.ou.edu/|http://www.nhn.ou.edu/|\\.jpg\\b|\\.pdf\\b)")

href_isWorking_map = get_href_IsWorking_map()
href_to_files_map = get_href_to_files_map()
print("Discovered " +
      str(len(items)) +
      " unique HTML files with domain www.nhn.ou.edu" +
      " and " +
      str(len(href_IsWorking_map.keys())) +
      " unique external links")
confirmWorking()

#print(file_to_hrefs_map)

def printStatusHistory(codes : List[str]) -> str:
    history = ""
    if len(codes) > 0:
        for code in codes:
            history = history + code + "->"
    return history


os.chdir("..") # will print to 'hrefs.txt' in the main directory
print("file, href, status history, exit status", file=open("hrefs.csv", "w"))
response_code = re.compile("\\d+", re.IGNORECASE)
for file in file_to_hrefs_map:
    for href in file_to_hrefs_map[file]:
        http_exit = str(href_isWorking_map.get(href)[0])
        history = ""
        for code in href_isWorking_map.get(href)[1]:
            try:
                number = response_code.search(str(code))
                history = history + str(number.group(0)) + "->" # pulls out only the number
            except:
                history = "ERR"
        print(file + ", " + href + "," + history + ", " + http_exit, file=open("hrefs.csv", "a"))
