# -*- coding: utf-8 -*-
"""
prepare our base sentiment files
http://kt.ijs.si/data/Emoji_sentiment_ranking/

"""

POSITIVE_EMOJI = ['๐','๐','๐','๐','๐','๐','๐','๐','๐','๐','๐',
    '๐','๐','๐','๐','๐','๐ค','๐','๐','๐','๐','๐','๐','๐ค','๐',
    '๐ธ','๐น','๐บ','๐ป','๐ผ','๐ฝ','๐ค ','๐คฃ','๐คค','๐คฉ','๐คช','๐ฅณ','๐ฅฐ','โบ๏ธ']
NEGATIVE_EMOJI = ['๐ค','๐','๐','๐ถ','๐','๐ฃ','๐ฅ','๐ฎ','๐ค','๐ฏ','๐ช',
    '๐ซ','๐ด','โน๏ธ','๐','๐','๐','๐','๐','๐','๐','๐ท','๐ค','๐ค','๐ฒ',
    '๐','๐','๐ค','๐ข','๐ญ','๐ฆ','๐ง','๐จ','๐ฉ','๐ฌ','๐ฐ','๐ฑ','๐ณ','๐ต',
    '๐ก','๐ ','๐ฟ','๐น','๐','โ ๏ธ','๐พ','๐ฟ','๐','๐คข','๐คฅ','๐คง','๐คจ','๐คฌ',
    '๐คฎ']
NEUTRAL_EMOJI = ['๐ค','๐ฃ๏ธ','๐ค','๐ฅ','๐บ','๐ป','๐ฝ','๐พ','๐ค','๐ฉ','๐คก',
    '๐คซ','๐คญ','๐คฏ','๐ง','๐ฅด','๐ฅต','๐ฅถ','๐ฅบ','๐ฅฑ']



import json
import pprint
from pathlib import Path

export = {}

path = Path('./', 'emoji.csv')
with path.open('r') as f:
    lines = f.readlines()

for line in lines:
    parts = line.split(',')
    code_point_str = f'{int(parts[0],16):04X}'

    scoreboard = {}
    scoreboard[parts[3]] = '-'
    scoreboard[parts[4]] = '='
    scoreboard[parts[5]] = '+'
    best_score = max(scoreboard.keys())
    winner = scoreboard[best_score]

    sentiment_score = parts[6]
    export[code_point_str] = {'sentiment': winner, 'sentiment_score': sentiment_score}

for emoji in POSITIVE_EMOJI:
    cp = ' '.join([f'{ord(c):04X}' for c in emoji])
    if not export.get(cp):
        export[cp] = {'sentiment': '+'}

for emoji in NEGATIVE_EMOJI:
    cp = ' '.join([f'{ord(c):04X}' for c in emoji])
    if not export.get(cp):
        export[cp] = {'sentiment': '-'}

for emoji in NEUTRAL_EMOJI:
    cp = ' '.join([f'{ord(c):04X}' for c in emoji])
    if not export.get(cp):
        export[cp] = {'sentiment': '='}

pp = pprint.pformat(export)
outfile = Path('./', 'sentiment.py')
with outfile.open('w', encoding='utf-8') as f:
    f.write(f'data = {pp}')

