from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.serebii.net'
GEN6_TITLES = []

def scrapeGen6(links, key):
    pokedex = {}
    a = set()
    for pokemon in links[key]:
        number = pokemon.split('/')[-1].split('.')[0]
        if not number.isdigit():
            continue
        html_result = requests.get(BASE_URL + pokemon)
        soup = BeautifulSoup(html_result.text, 'lxml')
        content_tables = soup.find_all('table', attrs={'class': 'dextable'})
        content_tables.pop(0)
        for table_count, table in enumerate(content_tables):
            table_rows = table.find_all('tr')
            content = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                content.append(row)
            a.add(str(content[0]))
            #idx = GEN3_TITLES.index(content[0])
            #content = cleanGen3(content, idx)
            #pokedex = addGen3(content, table_rows, idx, pokedex, number)
    print(a)
    return pokedex