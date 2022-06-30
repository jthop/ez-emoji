# -*- coding: utf-8 -*-
"""
prepare our base sentiment files
http://kt.ijs.si/data/Emoji_sentiment_ranking/

"""

POSITIVE_EMOJI = ['😀','😁','😂','😃','😄','😅','😆','😉','😊','😋','😎',
    '😍','😘','😗','😙','😚','🤗','😇','😏','😌','😛','😜','😝','🤑','😈',
    '😸','😹','😺','😻','😼','😽','🤠','🤣','🤤','🤩','🤪','🥳','🥰','☺️']
NEGATIVE_EMOJI = ['🤔','😐','😑','😶','🙄','😣','😥','😮','🤐','😯','😪',
    '😫','😴','☹️','🙁','😒','😓','😔','😕','😖','🙃','😷','🤒','🤕','😲',
    '😞','😟','😤','😢','😭','😦','😧','😨','😩','😬','😰','😱','😳','😵',
    '😡','😠','👿','👹','💀','☠️','😾','😿','🙀','🤢','🤥','🤧','🤨','🤬',
    '🤮']
NEUTRAL_EMOJI = ['🤓','🗣️','👤','👥','👺','👻','👽','👾','🤖','💩','🤡',
    '🤫','🤭','🤯','🧐','🥴','🥵','🥶','🥺','🥱']



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

