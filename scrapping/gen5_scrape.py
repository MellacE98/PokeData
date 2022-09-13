from bs4 import BeautifulSoup
import requests
import copy

BASE_URL = 'https://www.serebii.net'
GEN5_TITLES = [['Images'],  # 0
               ['Name', 'Other Names', 'No.', 'Gender Ratio', 'Type'],
               ['\n\t\tDamage Taken\n\t\t'],
               ['Wild Hold Item', 'Egg Groups'],
               ['Evolutionary Chain'],
               ['Locations - In-Depth Details'],
               ['Locations'],
               ['Flavor Text'],
               ['Alternate Forms'],  # 8
               #
               # MOVEMENTS
               #
               ['Black 2/White 2 Level Up'],  # 9
               ['Black/White Level Up - Sky Forme'],
               ['Black/White Level Up - Trash Cloak'],
               ['Black/White Level Up - Pirouette Forme'],
               ['Pre-Evolution Only Moves'],
               ['Black/White Level Up'],
               ['Black 2/White 2 Level Up - White Kyurem'],
               ['Special Moves'],
               ['TM & HM Attacks'],
               ['Black 2/White 2 Level Up - Black Kyurem'],
               ['Egg Moves (Details)'],
               ['Gen III & IV Only Moves (Details)'],
               ['Black/White Level Up - Zen Mode'],
               ['Black/White/Black 2/White 2 Level Up'],
               ['Black/White Level Up - Defense Forme'],
               ['Black/White Level Up - Sandy Cloak'],
               ['Black 2/White 2 Move Tutor Attacks'],
               ['Black/White Level Up - Attack Forme'],
               ['Black/White Level Up - Speed Forme'],
               ['Gen IV Only Moves (Details)'],
               ['Move Tutor Attacks'],  # 29
               #
               # STATS
               #
               ['Stats'],  # 30
               ['Stats - Zen Mode'],
               ['Stats - Sky Forme'],
               ['Stats - Sandy Cloak'],
               ['Stats - Attack Forme'],
               ['Stats - Alternate Forms'],
               ['Stats - Therian Forme'],
               ['Stats - Speed Forme'],
               ['Stats - Black Kyurem'],
               ['Stats - Defense Forme'],
               ['Stats - White Kyurem'],
               ['Stats - Origin Forme'],
               ['Stats - Pirouette Forme'],
               ['Stats - Trash Cloak']]  # 43


def scrapeGen5(links, key):
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
            idx = GEN5_TITLES.index(content[0])
            pokedex = addGen5(content, idx, table_rows, pokedex, number)
    return pokedex


def addGen5(content, idx, table_rows, pokedex, number):
    if idx == 0:
        pass

    elif idx == 1:
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

            elif 'abilities:' in lower_content:
                pokedex[number]['abiliy_1'] = None
                pokedex[number]['abiliy_2'] = None
                pokedex[number]['hidden_ability'] = None
                abilities = lower_content.replace('\n', '').split('abilities: ')[1]
                abilities = abilities.split('-')
                for ab_count, ability in enumerate(abilities):
                    if 'hidden ability' in ability:
                        pokedex[number]['hidden_ability'] = ability.replace('(hidden ability)', '').strip()
                    else:
                        pokedex[number]['abiliy_'+str(ab_count+1)] = ability.strip()

            elif 'classification' in lower_content:
                pokedex[number]['classification'] = content[count + 1][0]
                height = content[count + 1][1].split("\n\t\t\t")
                height[1] = height[1].replace('m', '')
                pokedex[number]['height'] = float(height[1])
                weight = content[count + 1][2].split("\n\t\t\t")
                weight[1] = weight[1].replace('kg', '')
                pokedex[number]['weight'] = float(weight[1])
                pokedex[number]['capture_rate'] = int(content[count + 1][3])
                pokedex[number]['base_egg_steps'] = int(content[count + 1][4].replace(',', ''))

            elif 'experience growth' in lower_content:
                experience = content[count + 1][0].split('Points')
                pokedex[number]['exp_growth'] = experience[0]
                pokedex[number]['exp_growth_type'] = experience[1]
                pokedex[number]['base_happiness'] = content[count + 1][1]
                pokedex[number]['flee_flag'] = content[count + 1][-2]
                pokedex[number]['entree_forest_level'] = content[count + 1][-1].replace('Level ', '')

        pokemon_types = table_rows[1].find_all('a')
        for count, i in enumerate(pokemon_types):
            type_found = i.get('href').split('/')[-1]
            type_found = type_found.split('.')[0]
            if type_found != 'na' and count < 2:
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
                pokedex[number]['egg_group_' + str(count + 1)] = group

    elif idx in [4, 5, 6, 7, 8]:
        pass

    elif idx == 30:
        for count, stat in enumerate(content[1]):
            if count != 0:
                pokedex[number]['base_' + stat.lower().replace('sp. ', 'sp_')] = content[2][count]

    elif idx == 31:
        pass
    elif idx == 32:
        pass
    elif idx == 33:
        pass
    elif idx == 34:
        pass
    elif idx == 35:
        pass
    elif idx == 36:
        pass
    elif idx == 37:
        pass
    elif idx == 38:
        pass
    elif idx == 39:
        pass
    elif idx == 40:
        pass
    elif idx == 41:
        pass
    elif idx == 42:
        pass
    elif idx == 43:
        pass
    else:
        pass

    return pokedex
