import sqlite3
from bs4 import BeautifulSoup
import requests
import re
import time
import sys, getopt
from random import uniform
import urllib.request
import json
import pprint as pp

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

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
        findContent(out_db, in_db)

# Reads search term from in_db, searchs imgur,
# adds resulting links to out_db
def findContent(out_db, in_db=""):
    print("STARTING IMAGE SEARCH, PLEASE WAIT")

    out_db = sqlite3.connect(out_db)
    out_c = out_db.cursor()
    out_c.execute('''CREATE TABLE IF NOT EXISTS imgs
        (link TEXT PRIMARY KEY,
        tag TEXT,
        FOREIGN KEY(tag) REFERENCES tags(tag))''')
    out_c.execute('''CREATE TABLE IF NOT EXISTS tags
        (tag TEXT PRIMARY KEY,
        related TEXT)''')
    out_db.commit()
    search_imgur(out_db)

def search_imgur(out_db):
    client_id = 'f2e81937fa7580c'
    client_secret = '2304d362e0fbc46ac9a9f14c7129a38a24264d30'

    client = ImgurClient(client_id, client_secret)

    out_c = out_db.cursor()
    try:
        queries = ['memes']
        for query in queries:
            tags = find_related_tags(query)
            tags = [query] + tags
            for tag in tags:
                check = out_c.execute('''SELECT * FROM tags WHERE tag=\'%s\'''' % tag).fetchone()
                if (check != None):
                    continue
                i = 0
                related = ','.join(find_related_tags(tag))
                values = (tag, related)
                out_c.execute('''INSERT OR IGNORE INTO tags(tag, related) VALUES(?, ?)''', values)
                out_db.commit()
                items = client.gallery_search(tag, advanced=None, sort='time', window='all', page=i)
                while len(items) != 0:
                    for item in items:
                        values = (item.link, tag)
                        out_c.execute('''INSERT OR IGNORE INTO imgs(link, tag) VALUES(?, ?)''', values)
                        out_db.commit()
                    i += 1
                    print(tag + ' Page ' + str(i))
                    items = client.gallery_search(tag, advanced=None, sort='time', window='all', page=i)
    except ImgurClientError as e:
        print(e.error_message)
        print(e.status_code)

def find_related_tags(query):
    url = "https://www.top-hashtags.com/hashtag/" + query
    page = requests.get(url).content
    soup = BeautifulSoup(page, "html.parser")
    alltags = []
    for tags in soup.findAll("div", {"class": "tht-tags"}):
        # split by " #" and remove first '#' and last ' '
        tags = tags.text.split(" #")
        tags[0] = tags[0][1:]
        tags[-1] = tags[0][:-1]
        alltags += tags
    return alltags

if __name__ == "__main__":
    processArguments(sys.argv[1:])
