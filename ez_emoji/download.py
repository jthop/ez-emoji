# -*- coding: utf-8 -*-
"""
"""
from datetime import datetime
from pathlib import Path
import json
import pprint
import re
import urllib.request

URL = 'https://unicode.org/Public/emoji/14.0/emoji-test.txt'


####################

emoji_line = r'(?P<code>.*)\s+;\s+(?P<qualification>.*)\s+#(?P<emoji>.*)\s+E\d+.\d+\s+(?P<name>.*)'
compiled = re.compile(emoji_line)
data = {}
small = {}
groups = {}
today = datetime.today().strftime("%m_%d_%Y")
data_directory = './data'
json_file = f'emoji_data_{today}.json'
min_json_file = f'min_emoji_data_{today}.json'

response = urllib.request.urlopen(URL)
for line in response:
    line = line.decode('utf-8')

    if '# group:' in line:
        group = line.split(':')[1].strip('\n').strip()

    if '# subgroup:' in line:
        subgroup = line.split(':')[1].strip('\n').strip()
        if groups.get(group):
            groups[group].append(subgroup)
        else:
            groups[group] = [subgroup]

    match = compiled.search(line)
    if match:
        q = match.group('qualification').strip()
        name = match.group('name').strip()
        code = match.group('code').strip()
        emoji = match.group('emoji').strip()
        key = name.replace(
            ' ', '_').replace("'",'').replace(':','').lower()

        if 'skin tone' in name:
            # skip these
            continue

        small[key] = emoji

        data[key] = {
            'code': code,
            'emoji': emoji,
            'name': name,
            'group': group,
            'subgroup': subgroup, 
            'status': q
        }

obj = {'groups': groups, 'emojis': data}

json_path = Path(data_directory, json_file)
with json_path.open('w', encoding='utf-8') as f:
    json.dump(obj, f)

min_path = Path(data_directory, min_json_file)
with min_path.open('w', encoding='utf-8') as f:
    json.dump(small, f)
