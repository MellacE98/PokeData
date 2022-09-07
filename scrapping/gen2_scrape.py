from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.serebii.net'
GEN2_TITLES = [['Name', 'Other Names', 'No.', 'Gender Ratio', 'Type'],
               ['Experience Growth', 'Base Happiness', 'Effort Values Earned'],
               ['\r\n\t\tDamage Taken\r\n\t\t'],
               ['Wild Hold Item', 'Egg Groups'],
               ['Evolutionary Chain'],
               ['Locations'],
               ['Locations - In-Depth Details'],
               ['Gen I Only Moves (Details)'],
               ['TM & HM Attacks'],
               ['Egg Moves (Details)'],
               ['Generation II Level Up'],
               ['Crystal Level Up'],
               ['Pre-Evolution Only Moves'],
               ['Crystal Move Tutor Attacks'],
               ['Gen I  Only Moves (Details)'],
               ['Gold & Silver Level Up'],
               ['Special Moves'],
               ['Stats']]


def scrapeGen2(links, key):
    pokedex = {}
    for pokemon in links[key]:
        number = pokemon.split('/')[-1].split('.')[0]
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
            idx = GEN2_TITLES.index(content[0])
            content = cleanGen2(content, idx)
            pokedex = addGen2(content, table_rows, idx, pokedex, number)
    return pokedex


def cleanGen2(content, idx):
    if idx == 0:
        if ' ' in content[1]:
            content[1].remove(' ')
        if '' in content[1]:
            content[1].remove('')
        if '%' in content[1][-1]:
            content[1] = [content[1][0], content[1][-8], float(content[1][-3].replace('%', '')), float(content[1][-1].replace('%', ''))]
        elif '%' not in content[1][-1]:
            content[1][-1] = [content[1][0], content[1][-4], 0.0, 0.0]
        content[-1][1] = content[-1][1].replace('\r\n\t\t\t', '').split('"')[1].replace('m', '')
        content[-1][2] = content[-1][2].replace('\r\n\t\t\t', '').split('lbs')[1].replace('kg', '')

    elif idx == 1:
        split_exp = content[1][0].split('Points')
        content[1][0] = int(split_exp[0].replace(',', '').replace(' ', ''))
        content[1].insert(1, split_exp[1])

    elif idx == 2:
        for count, value in enumerate(content[-1]):
            content[-1][count] = value.replace('*', '')

    elif idx in [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]:
        pass

    return content


def addGen2(content, table_rows, idx, pokedex, number):
    if idx == 0:
        pokedex[number] = {}

        pokedex[number]['number'] = number.replace('#', '')
        pokedex[number]['name'] = content[1][0]
        pokedex[number]['male_ratio'] = content[1][-2]
        pokedex[number]['female_ratio'] = content[1][-1]
        pokedex[number]['classification'] = content[-1][0]
        pokedex[number]['height'] = content[-1][1]
        pokedex[number]['weight'] = content[-1][2]
        pokedex[number]['capture_rate'] = content[-1][3]
        pokedex[number]['base_egg_steps'] = int(content[-1][-1].replace(',', ''))

        pokedex[number]['type_1'] = None
        pokedex[number]['type_2'] = None
        for count, i in enumerate(table_rows[1].find_all('a')):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            pokedex[number]['type_' + str(count + 1)] = type_found

    elif idx == 1:
        pokedex[number]['exp_growth'] = content[-1][0]
        pokedex[number]['exp_growth_type'] = content[-1][1]
        pokedex[number]['base_happiness'] = int(content[-1][2])

    elif idx == 2:
        for type_count, i in enumerate(table_rows[1].find_all('a')):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            pokedex[number]['against_' + type_found] = content[-1][type_count]

    elif idx == 3:
        pokedex[number]['egg_group'] = content[1][-1]

    elif idx == 17:
        for count, stat in enumerate(content[1]):
            if count != 0:
                pokedex[number]['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]

    elif idx in [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]:
        pass

    return pokedex
