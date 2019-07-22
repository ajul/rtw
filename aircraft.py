import os
import re

data_dir = 'C:/NWS/Rule the Waves 2/Data'

# plane type -> tuple
data = {}

def interpret_data(stats):
    max_speed = stats[1]
    cruise_speed = stats[2]
    
    l_range = stats[5]
    m_range = stats[6]
    h_range = stats[7]

    firepower = stats[8]
    maneuverability = stats[9]
    toughness = stats[10]

    maintenance_carrier = stats[11] #?
    maintenance_land = stats[12] #?
    
    l_bomb = stats[14]
    m_bomb = stats[15]
    h_bomb = stats[16]
    torpedo = stats[17]
    
    radar = stats[19]
    spotting = stats[20]
    attack_profile = stats[21] # ?

with open(os.path.join(data_dir, 'AircraftBasicData.dat')) as f:
    for line in f:
        tokens = line.rstrip().split(';')
        if len(tokens) == 1:
            plane_type = tokens[0]
            data[plane_type] = []
        elif len(tokens) == 22:
            data[plane_type].append(tokens)
        else:
            raise Exception('Unrecognized token count %d' % len(tokens))

result = ''
for plane_type, models in data.items():
    if len(models) == 0: continue
    result += '=== %s ===\n' % plane_type[1:-1].title()
    result += '{| class = "wikitable"\n'
    result += '! rowspan = "2" | Year \n'
    result += '! colspan = "2" | Speed \n'
    result += '! rowspan = "2" | ?3 \n'
    result += '! rowspan = "2" | ?4 \n'
    result += '! colspan = "3" | Range \n'
    result += '! rowspan = "2" | Fpw \n'
    result += '! rowspan = "2" | Mnv \n'
    result += '! rowspan = "2" | Tgh \n'
    result += '! rowspan = "2" | ?11 \n'
    result += '! rowspan = "2" | ?12 \n'
    result += '! rowspan = "2" | ?13 \n'
    result += '! colspan = "3" | Bomb \n'
    result += '! rowspan = "2" | Trp \n'
    result += '! rowspan = "2" | ?18 \n'
    result += '! rowspan = "2" | Radar \n'
    result += '! rowspan = "2" | ?20 \n'
    result += '! rowspan = "2" | ?21 \n'
    result += '|-\n'
    result += '! Max \n'
    result += '! Cru \n'
    result += '! L \n'
    result += '! M \n'
    result += '! H \n'
    result += '! L \n'
    result += '! M \n'
    result += '! H \n'
    for idx, stats in enumerate(models):
        if stats[1] == '-': continue
        result += '|-\n'
        result += '| ' + ' || '.join(stats) + '\n'
    result += '|}\n'

with open('aircraft.txt', mode='w') as outfile:
    outfile.write(result)
            
