import os
import re

data_dir = 'C:/NWS/Rule the Waves 2/Data'

categories = {}

with open(os.path.join(data_dir, 'ResearchAreas2.dat')) as f:
    for line in f:
        tokens = line.rstrip().split(';')
        if len(tokens) == 1:
            if 'PicName' in tokens[0]: continue
            category = tokens[0]
            categories[category] = []
        elif len(tokens) == 7:
            categories[category].append(tokens)
        else:
            raise Exception('Unrecognized token count %d' % len(tokens))

result = ''
for category, techs in categories.items():
    print(category)
    category_name = re.match('\[(.*) \d+\]', category).group(1)
    result += '=== %s ===\n' % category_name
    result += '{| class = "wikitable"\n'
    result += '! Lv. \n'
    result += '! style = "width:50%;" | Tech \n'
    result += '! Year \n'
    result += '! ? \n'
    result += '! ? \n'
    result += '! ? \n'
    result += '! style = "width:50%;" | Effect\n'
    for idx, (tech, year, a, b, c, index, effect) in enumerate(techs):
        result += '|-\n'
        result += '| ' + ' || '.join((str(idx + 1), tech, year, a, b, c, effect)) + '\n'
    result += '|}\n'

with open('techs.txt', mode='w') as outfile:
    outfile.write(result)
