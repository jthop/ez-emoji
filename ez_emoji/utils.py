import random
import json
from pathlib import Path
import copy

GOOD_EMOJIS = [
    'thumbs_up',
	'clapping_hands',
	'folded_hands', 
	'raised_fist',
	'flexed_biceps',
    'smiling_face_with_sunglasses',
    'star-struck',
    'crown', 
    'fire', 
    'bullseye', 
    'taco', 
    'glowing_star', 
    'hundred_points', 
    'high_voltage', 
    'kiss_mark', 
    'party_popper', 
    'partying_face',
    'rocket',
    'pizza',
    'clinking_glasses',
	'cherries',
	'1st_place_medal',
	'chart_increasing',
]

BAD_EMOJIS = [
	'scorpion',
	'snake',
	'skull_and_crossbones',
	'skull',
	'skunk',
	'vampire',
	'weary_cat',
	'collision',
	'weary_face',
	'angry_face',
	'frowning_face',
	'frowning_face_with_open_mouth',
	'thumbs_down', 
	'toilet'
]

COLLECTIONS = {
	'gun_to_the_head': ['water_pistol', 'weary_face'],
	'gamble': ['crossed_fingers', 'game_die'],
	'old_school': ['floppy_disk', 'videocassette', 'video_game', 'video_camera', 'pager'],
	'security': [
		'key', 'old_key', 'police_car', 'police_officer', 'police_car_light'
	],
	'phones': ['telephone', 'telephone_receiver'],
	'winter': ['snowman', 'snowflake', 'skier'],
	'vacation': ['palm_tree', 'man_surfing', 'beach_with_umbrella', 'passenger_ship', 'tropical_drink'],
	'money': ['money_with_wings', 'money_bag', 'heavy_dollar_sign', 'dollar_banknote'],
	'sports': ['man_golfing', 'man_running', 'man_lifting_weights', 'curling_stone', 'basketball'],
    'love': ['peach', 'high-heeled_shoe', 'lipstick', 'kiss', 'red_heart', 'tongue']
}


p = Path('emoji_data.json')
with p.open('r') as f:
	data = json.load(f)
emoji_data = data['emojis']
group_data = data['groups']

#################


def load_emoji(short_name):
	"""load emoji based on key
	"""
	code = emoji_data.get(short_name)
	if code:
		return code


def print_all():
	"""print all emojis in batches of 5
	"""
	l = [f"{k[:10]} = {v['emoji']}" for k,v in emoji_data.items()]
	result = tuple(l[x:x + 5] for x in range(0, len(l), 5))
	for group in result:
		print(group)


def rnd_good_emoji(qty=1):
	"""random good emoji - good is defined in constants
	"""
	results = []
	for n in range(qty):
		r = random.randint(1,len(GOOD_EMOJIS))
		key = GOOD_EMOJIS[r-1]
		results.append(emoji_data[key])
	return ''.join([x for x in results])


def rnd_bad_emoji(qty=1):
	"""random bad emoji - bad is defined in constants
	"""
	results = []
	for n in range(qty):
		r = random.randint(1,len(BAD_EMOJIS))
		key = BAD_EMOJIS[r-1]
		results.append(emoji_data[key])

	return ''.join([x for x in results])

print_all()
