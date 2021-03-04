import os
from SiteTools import *
#from Physics.SiteTools import expandDir, filterHTML


os.chdir("www.nhn.ou.edu")
dir_contents = os.listdir()
dir_contents = expandFilePaths(dir_contents)    # 1. gets path of all files

items = filterHTML(dir_contents)          # 2. reads each file to determine HTML
build_href_maps(items, ignore="(@|/|https://www.nhn.ou.edu/|http://www.nhn.ou.edu/|\\.jpg\\b|\\.pdf\\b)")

print("Discovered " +
      str(len(href_IsWorking_map.keys())) +
      " unique external links")

os.chdir("..") # will print to 'hrefs.txt' in the main directory
print_status_by_site()
print_status_by_href()

#print(file_to_hrefs_map)



