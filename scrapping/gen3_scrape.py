import copy

from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.serebii.net'
GEN3_TITLES = [['Pokémon Game Picture', 'National No.', 'Hoenn No.', 'English name', 'Japanese Name'],
               ['Wild Hold Item', 'Dex Category', 'Colour Category', 'Footprint'],
               ['\n\t\tDamage Taken\n\t\t'],
               ['\n\t\tFlavor Text\n\t\t'],
               ['\nLocation\n'],
               ['Fire Red/Leaf Green/Emerald Tutor Attacks'],
               ['Special Attacks'],
               [],
               ['Emerald Tutor Attacks'],
               ['Egg Moves'],
               ['Egg Steps to Hatch', 'Effort Points from Battling it', 'Catch Rate'],
               ['Egg Groups'],
               ['Stats (Attack form)'],
               ['Stats (Speed form)'],
               ['Stats (Defence Form)'],
               ['Stats']]


def scrapeGen3(links, key):
    pokedex = {}
    for pokemon in links[key]:
        print(pokemon)
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
            idx = GEN3_TITLES.index(content[0])
            content = cleanGen3(content, idx)
            pokedex = addGen3(content, table_rows, idx, pokedex, number)
    return pokedex


def cleanGen3(content, idx):
    if idx == 0:
        if ' ' in content[1]:
            content[1].remove(' ')
        if '' in content[1]:
            content[1].remove('')
        if '\n' in content[1]:
            content[1].remove('\n')
        for i in content:
            if i == ['\n', '']:
                content.remove(i)
        content[1] = [content[1][1].replace('\n\t\t', ''), content[1][3].replace('\n\t\t', '')]
        content[2] = [content[2][-1].replace('\n', '').split('Ability: ')[1]]
        if len(content[5]) == 1:
            male = 0.0
            female = 0.0
        else:
            male = content[5][0].replace('\n\t\t', '').split('Male: ')[1].replace('%', '').replace(' ', '')
            female = content[5][1].replace('\n\t\t', '').split('Female: ')[1].replace('%', '').replace(' ', '')
        content[5] = [male, female]
        if len(content[-1]) == 5 and len(content) == 10:
            height = content[-1][-2].replace('\n\t\t', '').split("\'")
            height[1] = height[1].replace('"', '')
            height_number = round((float(height[0]) * 30.48 + float(height[1]) * 2.54) / 100, 2)
            weight = round(float(content[-1][-1].replace('\n\t\t', '').split(' ')[0].replace(',', '')) * 0.45359237, 2)
            content[-1] = [content[-1][0].replace('\n\t\t', ''), height_number, weight]
        else:
            height = content[7][-2].replace('\n\t\t', '').split("\'")
            height[1] = height[1].replace('"', '')
            height_number = round((float(height[0])*30.48 + float(height[1])*2.54) / 100, 2)
            weight = round(float(content[7][-1].replace('\n\t\t', '').split(' ')[0].replace(',', ''))*0.45359237, 2)
            content[7] = [content[7][0].replace('\n\t\t', ''), height_number, weight]

    elif idx == 2:
        for count, value in enumerate(content[-1]):
            content[-1][count] = value.replace('*', '')

    elif idx == 10:
        content[-1][-1] = content[-1][-1].replace('\n\t\t', '')
        content[-1][0] = content[-1][0].replace('\n\t\t', '').lower().split(' ')[0]

    elif idx in [1, 3, 4, 5, 6, 7, 8, 9, 11, 15]:
        pass

    return content


def addGen3(content, table_rows, idx, pokedex, number):
    if idx == 0:
        pokedex[number] = {}

        pokedex[number]['number'] = number.replace('#', '')
        pokedex[number]['name'] = content[1][1]
        abilities = content[2][0].split('&')
        pokedex[number]['ability_1'] = None
        pokedex[number]['ability_2'] = None
        for count, ability in enumerate(abilities):
            pokedex[number]['ability_'+str(count+1)] = ability.strip()
        pokedex[number]['male_ratio'] = content[5][0]
        pokedex[number]['female_ratio'] = content[5][1]
        if number != '386':
            pokedex[number]['classification'] = content[7][0]
            pokedex[number]['height'] = content[7][1]
            pokedex[number]['weight'] = content[7][2]
        else:
            pokedex[number]['classification'] = content[-1][0]
            pokedex[number]['height'] = content[-1][1]
            pokedex[number]['weight'] = content[-1][2]

        pokedex[number]['type_1'] = None
        pokedex[number]['type_2'] = None

        pokemon_types = table_rows[9].find_all('a')
        if len(pokemon_types) == 0:
            pokemon_types = table_rows[10].find_all('a')
        if number == '386':
            pokemon_types = table_rows[13].find_all('a')
        for count, i in enumerate(pokemon_types):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            if type_found != 'na':
                pokedex[number]['type_' + str(count + 1)] = type_found

    elif idx == 2:
        for type_count, i in enumerate(table_rows[1].find_all('a')):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            pokedex[number]['against_' + type_found] = content[-1][type_count]

    elif idx == 10:
        pokedex[number]['base_egg_steps'] = content[-1][0]
        pokedex[number]['capture_rate'] = content[-1][-1]

    elif idx == 11:
        pokedex[number]['egg_group_2'] = None
        pokedex[number]['egg_group_1'] = None
        if len(content[-1]) == 2:
            pokedex[number]['egg_group_1'] = content[-1][1]
        if len(content) == 4:
            pokedex[number]['egg_group_2'] = content[-2][1]

    elif idx == 12:
        deoxys_attack = copy.deepcopy(pokedex['386'])
        deoxys_attack['name'] = deoxys_attack['name'] + '_attack'
        for count, stat in enumerate(content[1]):
            if count != 0:
                deoxys_attack['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex['386_a'] = deoxys_attack

    elif idx == 13:
        deoxys_speed = copy.deepcopy(pokedex['386'])
        deoxys_speed['name'] = deoxys_speed['name'] + '_speed'
        for count, stat in enumerate(content[1]):
            if count != 0:
                deoxys_speed['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex['386_s'] = deoxys_speed

    elif idx == 14:
        deoxys_defense = copy.deepcopy(pokedex['386'])
        deoxys_defense['name'] = deoxys_defense['name'] + '_defense'
        for count, stat in enumerate(content[1]):
            if count != 0:
                deoxys_defense['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex['386_d'] = deoxys_defense

    elif idx == 15:
        for count, stat in enumerate(content[1]):
            if count != 0:
                pokedex[number]['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]

    elif idx in [1, 3, 4, 5, 6, 7, 8, 9]:
        pass

    return pokedex
