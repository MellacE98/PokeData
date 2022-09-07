import pandas as pd
from bs4 import BeautifulSoup
import requests
from gen1_scrape import *
from gen2_scrape import *
from gen3_scrape import *
from gen4_scrape import *
from gen5_scrape import *
from gen6_scrape import *
from gen7_scrape import *
from gen8_scrape import *

BASE_URL = 'https://www.serebii.net'
GEN_NAME = ['pokedex',
            'pokedex-gs',
            'pokedex-rs',
            'pokedex-dp',
            'pokedex-bw']
""",
            
            'pokedex-xy',
            'pokedex-sm',
            'pokedex-swsh']"""


def getPokedexLinks():
    gens = {}
    for gen in GEN_NAME:
        gens[gen] = set()
        html_result = requests.get(BASE_URL + '/' + gen)
        soup = BeautifulSoup(html_result.text, 'lxml')
        for pkmn in soup.select('option[value*="/' + gen + '/"]'):
            link = pkmn.get('value')
            if '/egg/' not in link:
                gens[gen].add(link)
    return gens


def scrapeAllGens():
    pass

pokedex_links = getPokedexLinks()
for gen_num, gen in enumerate(GEN_NAME):
    if gen_num in [0, 1, 2, 3]:
        continue
    else:
        f_call = 'scrapeGen' + str(gen_num + 1) + '(pokedex_links, gen)'
        pokedex = eval(f_call)
        df = pd.DataFrame.from_dict(pokedex, orient='index')
        file_name = 'datasets/gen'+str(gen_num + 1)+'_pokedex.csv'
        df.to_csv(file_name, sep=',', encoding='utf-8', index=False)
