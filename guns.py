import os
import csv

data_dir = 'C:/NWS/Rule the Waves 2/Data'

class Calibre():
    def set_gundata(self, row):
        self.projectile_weight = row[1]
        self.rate_of_fire = row[2]
        self.max_range = row[3]

    def set_ordnance(self, row):
        self.category = row[1]
        self.gun_weight = int(row[2])
        self.cost = int(row[3])
        self.turret_weight_1 = int(row[4])
        self.turret_weight_2 = int(row[5])
        self.turret_weight_3 = int(row[6])
        if row[7] == 'x':
            self.casemate_weight = None
        else:
            self.casemate_weight = int(row[7])
        self.ammunition_weight = int(row[8])

    def set_vpen(self, row):
        self.vpen = [(int(x) if x else 0) for x in row[3:]]

    def set_hpen(self, row):
        self.hpen = [(int(x) if x else 0) for x in row[3:]]

calibres = { x : Calibre() for x in range(2, 21) }

with open(os.path.join(data_dir, 'Gundata.dat')) as gundata_file:
    reader = csv.reader(gundata_file, delimiter='\t')
    for row in reader:
        try:
            calibres[int(row[0])].set_gundata(row)
        except:
            pass

with open(os.path.join(data_dir, 'OrdnanceTable.dat')) as ordnance_file:
    reader = csv.reader(ordnance_file, delimiter='\t')
    for row in reader:
        try:
            calibres[int(row[0])].set_ordnance(row)
        except:
            pass

with open(os.path.join(data_dir, 'vpen.dat')) as vpen_file:
    reader = csv.reader(vpen_file, delimiter='\t')
    for row in reader:
        try:
            calibres[int(row[0])].set_vpen(row)
        except:
            pass
    
with open(os.path.join(data_dir, 'hpen.dat')) as hpen_file:
    reader = csv.reader(hpen_file, delimiter='\t')
    for row in reader:
        try:
            calibres[int(row[0])].set_hpen(row)
        except:
            pass

def pen_table(attr):
    result = '<table style="text-align:right;">\n'
    result += '<tr>'
    result += '<th rowspan="2">Range (kyd)</th>'
    result += '<th colspan="17" style="text-align:center;">Calibre</th>'
    result += '</tr>\n'
    result += '<tr>'
    for calibre in range(4, 21):
        result += '<th style="width:24pt;">%d"</th>' % calibre
    result += '</tr>\n'
    for r in range(1, 31):
        result += '<tr>'
        result += '<th>%d</th>' % r
        for calibre in range(4, 21):
            pen = getattr(calibres[calibre], attr)[r-1]
            if pen > 0:
                result += '<td>%d</td>' % pen
            else:
                result += '<td></td>'
        result += '</tr>\n'
    result += '</table>'

    return result

with open('vpen.txt', mode = 'w') as vpen_out:
    vpen_out.write(pen_table('vpen'))

with open('hpen.txt', mode = 'w') as hpen_out:
    hpen_out.write(pen_table('hpen'))
