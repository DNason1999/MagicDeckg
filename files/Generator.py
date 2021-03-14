import pandas as pd
import random
import os
from collections import Counter 
import datetime

df = pd.read_csv('transcribed_cards.csv')

print('Loaded Dataframe\n')

df = df.infer_objects()

with open('colors_combos.txt', 'r') as f:
    colors_combos = [x[:-1] for x in f.readlines()]
    colors_combos.append('')

print('Loaded Color Combos from file\n')

def get_colors(deck_df):
    colors_in_deck = {'R':0,'U':0,'W':0,'G':0,'B':0,'C':0}
    for x in deck_df['colors']:
        try:
            x = eval(x)
            if len(x) > 0:
                for color in x:
                    colors_in_deck[color] += 1
            else:
                colors_in_deck['C'] += 1
        except Exception as e:
            print(f'Exception is {e}')
            colors_in_deck['C'] += 1
    
    return {x:colors_in_deck[x]//2 for x in colors_in_deck}

def output_deck(deck_df):
    lands = get_colors(deck_df)
    k = Counter(lands)
    name = ''.join([x[0] for x in k.most_common(3)])

    card_name = f'd{datetime.datetime.now().day}'+f'ms{datetime.datetime.now().microsecond}'

    with open(f'decks/{name}_{card_name}.txt', 'w') as f:
        print(f'Deck Name: {f"{name}_{card_name}"}')
        for name,value in deck_df['name'].value_counts().iteritems():
            f.write(f'{value} {name}\n')
        counter = 0
        for x in lands:
            if counter + lands[x] > 20:
                f.write(f'{20 - counter} {land_names_mapping[x]}\n')
                break
            else:
                f.write(f'{lands[x]} {land_names_mapping[x]}\n')
                counter += lands[x]
            
def elements_in_list(one, two):
    colors_in_row = [key for key in one.keys() if one[key] == 1]
    for x in colors_in_row:
        if x not in two:
            return False
    return True

def get_input(msg, default_value, expected_output=None):
    counter = 0
    value = default_value
    while True:
        try:
            value = input(msg)
            if expected_output != None:
                if value not in expected_output:
                    value = 'error'
        except Exception as e:
            value = 'error'
        if value != 'error' and value != '':
            return value
        if value == '':
            return default_value
        if counter < 1:
            print(f'Incorrect input, you have {2-counter} chances before defaulting')
            counter += 1
        else:
            value = default_value
            break
    
    return value
        

print('Defined Functions\n')

legality = None
accepted_input = ['standard', 'future', 'historic','gladiator', 'pioneer', 'modern', 'legacy', 'pauper', 'vintage','penny', 'commander', 'brawl', 'duel', 'oldschool', 'premodern','']

legality = get_input('Enter legality, press enter for modern',
                        'modern',
                        accepted_input)

print(legality)

print('')

df = df.loc[df[legality] == 1]

print('Seperated Selected Legality Cards\n')

keep_columns = ['id','name','scryfall_uri','cmc','colors','color_identity','set','rarity','power','toughness','loyalty','legalities','card_faces','type_line','R','G','B','U','W']

df = df[keep_columns]

print('Filtered Columns\n')

land_names_mapping = {'R':'Mountain', 'G':'Forest','U':'Island','B':'Swamp','W':'Plains', 'C':'Wastes'}

colors = ['R','G','U','B','W']

print('Defined land names mapping and colors list\n')

counter = 0
selected_colors_input=None

selected_colors_input = get_input('Enter colors for your deck seperated by commas (i.e R,G,B ), press enter for random colors',
                        '',
                        colors_combos)

if selected_colors_input != '':
    try:
        selected_colors = eval('['+selected_colors_input+']')
    except Exception as e:
        print('Problem encountered evaluating input, resorting to random colors')
        selected_colors_input = ''
    
if selected_colors_input == '':
    num_colors = random.randint(10,50)//10
    selected_colors = random.sample(colors,num_colors)

print(f'Selected Colors: {selected_colors}')
selected_color_cards = df.loc[[elements_in_list(row, selected_colors) for index,row in df[colors].iterrows()]]

print(f'Remaining Cards shape: {selected_color_cards.shape}')

print('Finished selecting colors and filtering cards for colors\n')

counter = 0
num_decks = 1

num_decks = eval(get_input('Enter number of decks to create, press enter for 1',
                        '1'))

for x in range(0,num_decks):
    output_deck(selected_color_cards.sample(n=40, replace=True)[['name','cmc','colors']])

os.system('cmd /k')