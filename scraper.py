from urllib.request import urlopen
from socket import timeout
from json import loads

API_KEY = '47a04b83'

def get_movie(id):
    try:
        response = urlopen('http://www.omdbapi.com/?i={}&apikey={}'.format(id, API_KEY), timeout = 1).read()
        content = loads(response)
        if content['Response'] != 'True':
            return None
        return str(response)
    except:
        return None

with open('movies', 'r') as f:
    contents = loads(f.read()[:-3] + ']')
    with open('descriptions', 'w') as wf:
        wf.write('[\n')
        for c in contents:
            r = get_movie(c)
            if r != None:
                wf.write(r + ',\n')
        wf.write('\n]')
