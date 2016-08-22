import sqlite3
import sys, getopt

from init_db import init_db
from search_imgur import search_imgur

#always use console encoding
enc = sys.stdout.encoding

# Function for reading command line arguments
def processArguments(argv):
    # Get optcodes and input from cammand line arguments
    opts, args = getopt.getopt(argv,"i:o:",["indb=","outdb="])
    in_db = ""
    out_db = ""
    for opt, arg in opts:
        if opt in ("-i", "--indb"):
            in_db = arg
        elif opt in ("-o", "--outdb"):
            out_db = arg
    if out_db == "":# or in_db == "":
        # <inputdb> - name of the search term db
        # <outputdb> - name of the output db file
        print ("Please use: python search_images.py -i <inputdb> -o <outputdb>")
    else:
        return (out_db, in_db)

# Reads search term from in_db, searchs imgur,
# adds resulting links to out_db
def findContent(out_db, in_db=""):
    out_db = sqlite3.connect(out_db)
    init_db(out_db)
    search_imgur(out_db)

if __name__ == "__main__":
    args = processArguments(sys.argv[1:])
    if args != None:
        print("STARTING IMAGE SEARCH, PLEASE WAIT")
        findContent(*args)
