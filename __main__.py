import os
from Physics.SiteTools import *
#from Physics.SiteTools import expandDir, filterHTML

os.chdir("Physics/www.nhn.ou.edu")
items = expandDir(os.listdir())    # 1. gets path of all files
items = filterHTML(items)          # 2. reads each file to determine HTML
scanHrefs(items, ignore="(@|/|https://www.nhn.ou.edu/|http://www.nhn.ou.edu/|\\.jpg\\b|\\.pdf\\b)")

hrefs_isWorking_map = get_href_IsWorking_map()
href_to_files_map = get_href_to_files_map()
print("Discovered " +
      str(len(items)) +
      " unique HTML files with domain www.nhn.ou.edu" +
      " and " +
      str(len(href_IsWorking_map.keys())) +
      " unique external links")

confirmWorking()
os.chdir("..")
print(href_IsWorking_map, file=open("hrefs.txt", "a"))