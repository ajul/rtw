import os
import re

data_dir = 'C:/NWS/Rule the Waves 2/Data'

class Event():
    target_nation_types = {
        -99 : None,
        7 : 'hostile',
        9 : 'any',
        11 : 'friendly',
        99 : None,
    }

    condition_types = {
        0 : None,
    }
    
    def __init__(self, tokens):
        self.options = []
        self.text = tokens[0]
        self.target_nation = int(tokens[1] or -99)
        if tokens[2]: raise Exception('Non-empty tokens[2]')
        if tokens[3]: raise Exception('Non-empty tokens[3]')
        if tokens[4]: raise Exception('Non-empty tokens[4]')
        self.condition = int(tokens[5] or -99)
        self.start_year = int(tokens[6])
        self.end_year = int(tokens[7])

    def emplace_option(self, tokens):
        self.options.append(EventOption(tokens))

    def main_string(self):
        result = event.text + '\n'
        if self.target_nation in self.target_nation_types:
            target_nation_string = self.target_nation_types[self.target_nation]
            if target_nation_string is not None:
                result += '* Target: %s nation\n' % target_nation_string
        else:
            result += '* Target: unknown target condition %d\n' % self.target_nation
        if self.condition in self.condition_types:
            condition_string = self.condition_types[self.condition]
            if condition_string is not None:
                result += '* Condition: %s\n' % condition_string
        else:
            result += '* Condition: unknown condition %d\n' % self.condition
        return result

class EventOption():
    tension_target_types = {
        0 : 'XX',
        99 : 'XX',
        10 : 'random nations',
        8 : 'a nation of your choice',
    }

    effect_types = {
        1 : 'technology exchanged with XX?',
        2 : 'alliance forms with XX',
        3 : 'build submarines quest',
        4 : 'half build submarines quest',
        5 : 'build destroyers quest',
        6 : 'half build destroyers quest',
        7 : 'build cruisers quest',
        8 : 'half build cruisers quest',
        10 : 'build battleships quest',
        11 : '-1 unrest?',
        12 : '+1 unrest?',
        13 : 'a nation steals a technology from you',
        15 : '-2 unrest?',
        20 : 'sabotage attempt happens',
        25 : 'normal chance of possession becoming independent from XX',
        26 : 'increased chance of possession becoming independent from XX',
        27 : 'decreased chance of possession becoming independent from XX',
        30 : 'cruiser gains experience?',
        31 : 'battleship gains experience?',
        40 : '(chance of?) disarmament conference',
        41 : '(high chance of?) disarmament conference',
        50 : 'high chance to end war in white peace?',
        51 : 'low chance to end war in white peace?',
        52 : 'low chance to end war in minor victory?',
        53 : 'high chance to end war in major defeat?',
        54 : 'low chance to end war in minor defeat?',
        55 : 'high chance to end war in minor victory?',
        56 : 'low chance to end war in major victory?',
        60 : 'low chance of army victory',
        61 : 'high chance of army victory',
        70 : 'lose possession to XX?',
    }
    
    def __init__(self, tokens):
        self.text = tokens[0]
        self.money = int(tokens[1])
        self.prestige = int(tokens[2] or 0)
        self.tension = int(tokens[3])
        self.tension_target = int(tokens[4])
        self.effect = int(tokens[5])

    def main_string(self):
        result = self.text
        effects = []
        if self.money:
            if abs(self.money) >= 100:
                effects.append('%+d national resources?' % (self.money // 100))
            else:
                effects.append('%+d budget' % self.money)
        if self.prestige:
            effects.append('%+d prestige' % self.prestige)
        if self.tension:
            effects.append('%+d tension to %s' % (self.tension, self.tension_target_types[self.tension_target]))
        if self.effect:
            if self.effect in self.effect_types:
                effect_string = self.effect_types[self.effect]
                if effect_string is not None: effects.append(effect_string)
            else:
                effects.append('unknown effect %d' % self.effect)
        result += ' (%s)' % (', '.join(effects) or 'no effect')
        return result

events = []

with open(os.path.join(data_dir, 'Events.dat')) as f:
    for line in f:
        tokens = line.rstrip().split(';')
        if len(tokens) == 8: 
            current_event = Event(tokens)
            events.append(current_event)
        elif len(tokens) == 6:
            if not tokens[0]: continue
            current_event.emplace_option(tokens)
        else:
            raise Exception('Unrecognized token count %d' % len(tokens))

result = ''
for index, event in enumerate(events):
    result += '== Event %d ==\n' % (index + 1)
    result += event.main_string()
    result += '=== Options ===\n'
    for option in event.options:
        result += '* %s\n' % option.main_string()

with open('events.txt', mode='w') as outfile:
    outfile.write(result)
