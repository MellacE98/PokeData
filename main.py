from scrapping.pokedex_scrapper import *

def main():
    pokedex_links = getPokedexLinks()
    for gen_num, gen in enumerate(GEN_NAME):
        if gen_num in [0]:
            continue
        else:
            f_call = 'scrapeGen' + str(gen_num + 1) + '(pokedex_links, gen)'
            pokedex = eval(f_call)
            print(pokedex)
            
    pass

if __name__ == "__main__":
    main()