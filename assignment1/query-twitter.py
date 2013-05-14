import urllib
import json

response = []
for n in range(10):
    query = json.load(urllib.urlopen("http://search.twitter.com/search.json?q=microsoft&page=" + str(n+1)))
    response += query['results']

for response in response:
    print response['text']
