#John Baldwin
# lab 5
#sources: https://www.tutorialspoint.com/python/os_walk.html
            #geeksforgeeks.org
            #https://www.geeksforgeeks.org/compare-two-files-line-by-line-in-python
            #https://docs.python.org/3/library/datetime.html
            #https://stackoverflow.com/questions/2918362/writing-string-to-a-file-on-a-new-line-every-time
            #https://docs.python.org/3/library/glob.html
            #https://stackoverflow.com/questions/6773584/how-are-glob-globs-return-values-ordered/6774404#6774404
            #https://stackoverflow.com/questions/30551945/how-do-i-get-python-to-read-only-every-other-line-from-a-file-that-contains-a-po
            #https://airbrake.io/blog/python/python-indexerror
            #https://linuxhint.com/difflib-module-python/
            #https://docs.python.org/3/library/difflib.html



#If I had the time to do this lab again I would have used a dictionary to link files to their hashes+timestamp

import os, hashlib, datetime
from difflib import Differ
import glob

ignore = ["/dev","/proc","/run","/sys","/tmp","/var/lib","/var/run"]
logTime = datetime.datetime.now()
logName = "log" + str(logTime)  + ".txt"

#file recursive search
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        file = os.path.join(root, name)
        f = open(logName,"a") #append to log file
        dateTime = datetime.datetime.now()
        f.write(file + ' ' + str(dateTime) + '\n')
        hash = hashlib.sha256(name.encode())
        dateTime = datetime.datetime.now()
        f.write("Hash: " + hash.hexdigest() + ' ' + str(dateTime) + '\n')
    for name in dirs:
        if name not in ignore:
            dir = os.path.join(root, name)
            dateTime = datetime.datetime.now()
            f.write(dir + ' ' + str(dateTime) + '\n')
f.close()

print("******************************************************************************")
print("******************************************************************************")
print("******************************************************************************")
print("***************************     SYSTEM REPORT    *****************************")
#compare to previous log IF ONE EXISTS

#most recent log is likely glob.glob('log*.txt')[-1]
#might need error handling for empty array ------------------------------------------does need error handling for IndexError: list index out of range

#find most recent log
logs = sorted(glob.glob('log*.txt'))
newLog = logs[-1]
try:
    oldLog = logs[-2] #error happens here the first time the file is run

    n = open(newLog, "r")
    nline = n.readlines()
    n.close()
    o = open(oldLog, "r")
    oline = o.readlines()
    o.close()

    newest = []
    for i in nline:
        newest.append(i[:-28])
    old = []
    for j in oline:
        old.append(j[:-28])


    d = Differ() # '-' means only in old, '+' means only in new
    difference = list(d.compare(old, newest))
    #difference = '\n'.join(difference)

    for x in difference:
        if ("+ ./" in x):
            print("File Added")
            print(x)
        if ("- ./" in x):
            print("File Deleted")
            print(x)

except IndexError:
    print("\n\n\n\n\n NO PREVIOUS LOG FILE TO COMPARE TO")

#logs have file name + time on odd lines; hashes on even lines
#for every even line in newLog, if the hash does not appear on oldLog, add file name (previos line [:-lengthOfDate]) to file added list FILE WAS ADDED
#repeat for every file in oldLog compared to newLog,m add results to file deleted list FILE WAS DELETED

#just hash will be [:64] since it is 64 characters long
