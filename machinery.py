import os
import csv
import re

data_dir = 'C:/NWS/Rule the Waves 2/Data'

speeds = None

data = {}

with open(os.path.join(data_dir, 'SpeedHPTable2.dat')) as f:
    reader = csv.reader(f, delimiter='\t')
    
    for row in reader:
        if speeds is None:
            speeds = [int(x) for x in row[1:]]
        else:
            kiloton = int(row[0])
            data[kiloton] = {}
            for index, cell in enumerate(row[1:]):
                speed = speeds[index]
                try:
                    hp = int(cell)
                except:
                    hp = -1
                data[kiloton][speed] = hp

result = '<table>\n'
result += '<tr>'
result += '<th rowspan="2">Displacmement<br/>(tons)</th>'
result += '<th colspan="%d">HP / ton</th>' % len(speeds)
result += '</tr>\n'

result += '<tr>'
for speed in speeds:
    result += '<th>%d kt</th>' % speed
result += '</tr>\n'

for kiloton, hps in data.items():
    result += '<tr>'
    result += '<th>%d 000</th>' % kiloton
    for speed in speeds:
        hp = hps[speed]
        if hp > 0:
            result += '<td>%0.2f</td>' % (hps[speed] / kiloton)
        else:
            result += '<td></td>'
    result += '</tr>\n'
result += '</table>\n'

print(result)
