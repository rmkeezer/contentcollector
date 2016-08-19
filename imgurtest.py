from imgurpython import ImgurClient
from imgurpython.helpers.error import ImgurClientError

client_id = 'f2e81937fa7580c'
client_secret = '2304d362e0fbc46ac9a9f14c7129a38a24264d30'

client = ImgurClient(client_id, client_secret)

try:
    q = 'memes'
    i = 150
    items = client.gallery_search(q, advanced=None, sort='time', window='all', page=i)
    while len(items) != 0:
        for item in items:
            print(item.link)
        i += 1
        items = client.gallery_search(q, advanced=None, sort='time', window='all', page=i)
except ImgurClientError as e:
    print(e.error_message)
    print(e.status_code)