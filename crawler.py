from urllib.request import urlopen
from socket import timeout
from json import dumps, loads

API_KEY = '47a04b83'
START_WORD = 'Batman'
MAX_PAGE = 5

search_dict = {}
result_dict = {}

total_searches = 0

class SearchResultItem:
    def __init__(self, title, id):
        self.title = title
        self.id = id

class SearchResult:
    def __init__(self, total, items):
        self.total = total
        self.items = items

def search(word, page):
    global total_searches
    if total_searches  > 99: return None
    try:
        contents = loads(urlopen('http://www.omdbapi.com/?s={}&page={}&apikey={}&type=movie'.format(word, str(page), API_KEY), timeout = 1).read())
    except:
        total_searches  += 1
        return None
    total_searches  += 1
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
            for i in range(2, min(int(total / 10), MAX_PAGE) + 1):
                result = search(word, i)
                if result != None:
                    movies += result.items
    return movies

def process_word_recursively(word, f, count = 1):
    if count > 10: return True
    if word in search_dict: return False

    search_dict[word] = True
    movies = deplete_word(word)

    for m in movies:
        id = m.id
        if id not in result_dict:
            f.write('"' + id + '",\n')
            result_dict[id] = True

    for m in movies:
        ts = m.title.split()
        print(ts)
        if len(ts) > 1 and process_word_recursively(ts[1], f, count + 1):
            break

    return False


with open('movies', 'w') as f:
    f.write('[')
    process_word_recursively(START_WORD, f)
    f.write(']')
