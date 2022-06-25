import random


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


#################


def load_emoji(short_name):
	code = EMOJIS.get(short_name)
	if code:
		return code

def print_samples():
	for k,v in EMOJIS.items():
		print(f'{k} - {v}')

def rnd_good_emoji(qty=1):
	"""
	"""
	results = []
	for n in range(qty):
		r = random.randint(1,len(GOOD_EMOJIS))
		key = GOOD_EMOJIS[r-1]
		results.append(EMOJIS[key])
	return ''.join([x for x in results])

def rnd_bad_emoji(qty=1):
	"""
	"""
	results = []
	for n in range(qty):
		r = random.randint(1,len(BAD_EMOJIS))
		key = BAD_EMOJIS[r-1]
		results.append(EMOJIS[key])

	return ''.join([x for x in results])