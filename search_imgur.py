from bs4 import BeautifulSoup
import requests
import time
import urllib.request

from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

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
                related = find_related_tags(tag)
                for rtag in related:
                    values = (tag, rtag)
                    out_c.execute('''INSERT OR IGNORE INTO related_tags(source, target) VALUES(?, ?)''', values)
                    out_db.commit()
                related = ','.join(related)
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