import copy

from bs4 import BeautifulSoup
import requests

BASE_URL = 'https://www.serebii.net'
GEN4_TITLES = [['Images'],
               ['Name', 'Jp. Name', 'No.', 'Gender Ratio', 'Type'],
               ['\n\t\tDamage Taken\n\t\t'],
               ['Wild Hold Item', 'Egg Groups'],
               ['Evolutionary Chain'],
               ['\nFlavour Text\n'],
               ['\nLocation (In-Depth Details)\n'],
               ['\nLocation\n'],
               ['Diamond/Pearl Level Up (Trash Cloak)'],
               ['Diamond/Pearl Level Up (Sandy Cloak)'],
               ['Diamond/Pearl Level Up (Attack Form)'],
               ['Diamond/Pearl Level Up (Speed Form)'],
               ['Diamond/Pearl Level Up (Defense Form)'],
               ['Special Moves'],
               ['Diamond/Pearl Level Up'],
               ['Diamond/Pearl/Platinum/HeartGold/SoulSilver Level Up (All  Forms)'],
               ['Diamond/Pearl/Platinum/HeartGold/SoulSilver Level Up'],
               ['TM & HM Attacks'],
               ['3rd Gen Only  Moves'],
               ['HGSS TM & HM Attacks'],
               ['Egg Moves (Details)'],
               ['Pre-Evolution Moves'],
               ['HeartGold/SoulSilver Level Up (Altered Forme & Origin Forme)'],
               ['HeartGold/SoulSilver Level Up'],
               ['Platinum/HeartGold/SoulSilver Level Up'],
               ['Diamond/Pearl/Platinum Level Up'],
               ['Platinum/HeartGold/SoulSilver Move Tutor Attacks'],
               ['Move Tutor Attacks'],
               ['Sky Forme Level Up'],
               ['HeartGold/SoulSilver Move Tutor Attacks'],
               ['Base/Max Pokéthlon Stats - Altered Forme'],
               ['Base/Max Pokéthlon Stats - (A-Z)'],
               ['Base/Max Pokéthlon Stats - Land Forme'],
               ['Base/Max Pokéthlon Stats - Normal, Fire, Ground, Rock'],
               ['Base/Max Pokéthlon Stats - Normal Forme'],
               ['Base/Max Pokéthlon Stats - Plant Cloak'],
               ['Base/Max Pokéthlon Stats'],
               ['Base/Max Pokéathlon Stats'],
               ['Stats'],
               ['Stats - Sky Forme'],
               ['Stats - Alternate Forms'],
               ['Alternate Forms'],
               ['Stats - Sandy Cloak'],
               ['Stats - Attack Forme'],
               ['Stats - Speed Forme'],
               ['Stats - Defense Forme'],
               ['Stats - Origin Forme'],
               ['Stats - Trash Cloak']]


def scrapeGen4(links, key):
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
            idx = GEN4_TITLES.index(content[0])
            print(content[0])
            pokedex = addGen4(content, idx, table_rows, pokedex, number)
    return pokedex


def addGen4(content, idx, table_rows, pokedex, number):
    if idx == 1:
        pokedex[number] = {}
        pokedex[number]['number'] = number
        pokedex[number]['name'] = content[1][0]
        male = 0.0
        female = 0.0
        for count, i in enumerate(content):
            lower_content = content[count][0].lower()
            if 'female:' in lower_content:
                female = content[count][1].replace('%', '')
                pokedex[number]['female_ratio'] = female

            elif 'male:' in lower_content:
                male = content[count][1].replace('%', '')
                pokedex[number]['male_ratio'] = male

            elif 'ability:' in lower_content:
                pokedex[number]['abiliy_1'] = None
                pokedex[number]['abiliy_2'] = None
                abilities = lower_content.replace('\n', '').split('ability: ')[1]
                abilities = abilities.split('&')
                for ab_count, ability in enumerate(abilities):
                    pokedex[number]['abiliy_'+str(ab_count+1)] = ability.strip()

            elif 'classification' in lower_content:
                pokedex[number]['classification'] = content[count+1][0]
                height = content[count+1][1].split("\'")
                height[1] = height[1].replace('"', '')
                pokedex[number]['height'] = round((float(height[0]) * 30.48 + float(height[1]) * 2.54) / 100, 2)
                pokedex[number]['weight'] = round(float(content[count+1][2].replace(',', '').replace('lbs', '')) * 0.45359237, 2)
                pokedex[number]['capture_rate'] = int(content[count+1][3])
                pokedex[number]['base_egg_steps'] = int(content[count+1][4].replace(',', ''))

            elif 'experience growth' in lower_content:
                experience = content[count + 1][0].split('Points')
                pokedex[number]['exp_growth'] = experience[0]
                pokedex[number]['exp_growth_type'] = experience[1]
                pokedex[number]['base_happiness'] = content[count + 1][1]
                pokedex[number]['colour'] = content[count + 1][-2]
                pokedex[number]['safari_zone_flee_rate'] = content[count + 1][-1]

        pokemon_types = table_rows[1].find_all('a')
        for count, i in enumerate(pokemon_types):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            if type_found != 'na':
                pokedex[number]['type_' + str(count + 1)] = type_found
            else:
                continue

    elif idx == 2:
        for count, value in enumerate(content[-1]):
            content[-1][count] = value.replace('*', '')
        for type_count, i in enumerate(table_rows[1].find_all('a')):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            pokedex[number]['against_' + type_found] = content[-1][type_count]

    elif idx == 3:
        pokedex[number]['egg_group_2'] = None
        pokedex[number]['egg_group_1'] = None
        egg_groups = set()
        for count, i in enumerate(content):
            if count != 0:
                egg_groups.add(i[-1])
        for count, group in enumerate(egg_groups):
            if 'cannot' not in group:
                pokedex[number]['egg_group_'+str(count+1)] = group

    elif idx == 38:
        for count, stat in enumerate(content[1]):
            if count != 0:
                pokedex[number]['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]

    elif idx == 39:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name']+'_sky'
        poke['number'] = poke['number'] + '.1'
        poke['type_2'] = 'flying'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.1'] = poke

    elif idx == 40:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_alternate'
        poke['number'] = poke['number'] + '.1'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.1'] = poke

    elif idx == 42:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_sandy'
        poke['number'] = poke['number'] + '.1'
        poke['type_2'] = 'ground'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.1'] = poke

    elif idx == 43:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_attack'
        poke['number'] = poke['number'] + '.1'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.1'] = poke

    elif idx == 44:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_speed'
        poke['number'] = poke['number'] + '.2'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.2'] = poke

    elif idx == 45:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_defense'
        poke['number'] = poke['number'] + '.3'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.3'] = poke

    elif idx == 46:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_origin'
        poke['number'] = poke['number'] + '.1'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.1'] = poke

    elif idx == 47:
        poke = copy.deepcopy(pokedex[number])
        poke['name'] = poke['name'] + '_trash'
        poke['number'] = poke['number'] + '.2'
        poke['type_2'] = 'steel'
        for count, stat in enumerate(content[1]):
            if count != 0:
                poke['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]
        pokedex[number + '.2'] = poke

    else:
        pass

    return pokedex
