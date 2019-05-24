from urllib.request import urlopen
from json import dumps, loads

API_KEY = '47a04b83'
START_WORD = 'Batman'
MAX_PAGE = 5

class SearchResultItem:
    def __init__(self, title, id):
        self.title = title
        self.id = id

class SearchResult:
    def __init__(self, total, items):
        self.total = total
        self.items = items

def search(word, page):
    contents = loads(urlopen('http://www.omdbapi.com/?s={}&page={}&apikey={}&type=movie'.format(word, str(page), API_KEY)).read())
    if contents['Response'] != 'True': return None
    else:
        items = []
        for item in contents['Search']:
            sri = SearchResultItem(item['Title'], item['imdbID'])
            items.append(sri)
        return SearchResult(int(contents['totalResults']), items)

def deplete_word(word):
    result = search(word, 1)
    movies = []
    if result != None:
        movies += result.items
        total = result.total
        if total >= 20:
            for i in range(2, min((total / 10) + 1, MAX_PAGE)):
                movies += search(word, i).items
    return movies

movies = deplete_word('Batman')

with open('movies', 'w') as f:
    f.write('[\n')
    for movie in movies:
        f.write('{"title": "' + movie.title + '", "id": "' + movie.id + '"},\n')
    f.write(']\n')
