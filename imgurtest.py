from imgurpython import ImgurClient

client_id = 'f2e81937fa7580c'
client_secret = '2304d362e0fbc46ac9a9f14c7129a38a24264d30'

client = ImgurClient(client_id, client_secret)

# Example request
items = client.gallery()
for item in items:
    print(item.link)