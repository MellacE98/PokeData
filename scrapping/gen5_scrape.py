from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.serebii.net'
GEN5_TITLES = [['Images'],
               ['Stats - Zen Mode'],
               ['Move Tutor Attacks'],
               ['Black/White Level Up - Sky Forme'],
               ['Black/White Level Up - Trash Cloak'],
               ['Black/White Level Up - Pirouette Forme'],
               ['Pre-Evolution Only Moves'],
               ['Wild Hold Item', 'Egg Groups'],
               ['Locations - In-Depth Details'],
               ['Black/White Level Up'],
               ['Black 2/White 2 Level Up - White Kyurem'],
               ['Stats - Sky Forme'],
               ['Alternate Forms'],
               ['Special Moves'],
               ['Black 2/White 2 Level Up'],
               ['\n\t\tDamage Taken\n\t\t'],
               ['Stats - Sandy Cloak'],
               ['Name', 'Other Names', 'No.', 'Gender Ratio', 'Type'],
               ['TM & HM Attacks'],
               ['Flavor Text'],
               ['Stats - Attack Forme'],
               ['Stats - Alternate Forms'],
               ['Black 2/White 2 Level Up - Black Kyurem'],
               ['Egg Moves (Details)'],
               ['Stats'],
               ['Stats - Therian Forme'],
               ['Stats - Speed Forme'],
               ['Evolutionary Chain'],
               ['Gen III & IV Only Moves (Details)'],
               ['Black/White Level Up - Zen Mode'],
               ['Black/White/Black 2/White 2 Level Up'],
               ['Locations'],
               ['Black/White Level Up - Defense Forme'],
               ['Stats - Black Kyurem'],
               ['Stats - Defense Forme'],
               ['Black/White Level Up - Sandy Cloak'],
               ['Stats - White Kyurem'],
               ['Stats - Origin Forme'],
               ['Black 2/White 2 Move Tutor Attacks'],
               ['Stats - Pirouette Forme'],
               ['Black/White Level Up - Attack Forme'],
               ['Black/White Level Up - Speed Forme'],
               ['Gen IV Only Moves (Details)'],
               ['Stats - Trash Cloak']]


def scrapeGen5(links, key):
    pokedex = {}
    for pokemon in links[key]:
        number = pokemon.split('/')[-1].split('.')[0]
        if not number.isdigit():
            continue
        html_result = requests.get(BASE_URL + pokemon)
        soup = BeautifulSoup(html_result.text, 'lxml')
        content_tables = soup.find_all('table', attrs={'class': 'dextable'})
        for table_count, table in enumerate(content_tables):
            table_rows = table.find_all('tr')
            content = []
            for tr in table_rows:
                td = tr.find_all('td')
                row = [i.text for i in td]
                content.append(row)
            idx = GEN5_TITLES.index(content[0])
            #content = cleanGen3(content, idx)
            #pokedex = addGen3(content, table_rows, idx, pokedex, number)

    return pokedex