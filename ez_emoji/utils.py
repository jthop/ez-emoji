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


##############################
#
# EZEmoji class
#
##############################


class EZEmoji(object):
    data_file = 'EZEMOJI_UNICODE.json'

    def __init__(self):
        """
        """
        # initialize some variables
        self.emoji_data = None
        self.groups = []
        self.subgroups = []
        self.subgroup_map = {}
        self.lookup_by_group = {}
        self.lookup_by_subgroup = {}
        self.lookup_by_annotation = {}

        # Find the data file and load it
        self._load_data()
        self._create_lookups()

        return


    def _load_data(self):
        dirs = [
            Path.cwd(),
            Path.cwd().parent,
            Path.cwd().parent.parent,
            Path.home()
        ]
        for dir in dirs:
            path = Path(dir, EZEmoji.data_file)
            if path.exists():
                with path.open('r') as f:
                    data = json.load(f)
                self.emoji_data = data['emojis']
                self.groups = data['groups']
                self.subgroup_map = data['subgroups']
                for v in self.subgroup_map.values():
                    self.subgroups.extend(v)
                break
        else:
            raise ValueError(f'Cannot find {EZEmoji.data_file}')

        return


    def _create_lookups(self):
        # search by group, subgroup, annotation
        for k, v in self.emoji_data.items():
            # result is (short_name, emoji)
            result = (k, v['emoji'])

            if not self.lookup_by_subgroup.get(v['subgroup']):
                self.lookup_by_subgroup[v['subgroup']] = []
            self.lookup_by_subgroup[v['subgroup']].append(result)

            if not self.lookup_by_group.get(v['group']):
                self.lookup_by_group[v['group']] = []
            self.lookup_by_group[v['group']].append(result)

            for a in v['annotations']:
                if not self.lookup_by_annotation.get(a):
                    self.lookup_by_annotation[a] = []
                self.lookup_by_annotation[a].append(result)
        return


    def get_emoji(self, short_name):
        """load emoji based on key
        """
        emoji = self.emoji_data.get(short_name)
        return emoji


    def _print_by_grouping(self, _grouping=None, lookup=None):
        """print all emojis for fun
        """
        if not _grouping or not hasattr(self, _grouping):
            raise ValueError(_grouping)
        grouping = getattr(self, _grouping)
        if lookup is None:
            raise ValueError(lookup)

        for g in grouping:
            vals = lookup.get(g)
            if vals is None:
                continue
            print(f'\n----==== {g} ====---- \n')
            for val in vals:
                print(f"{val[0]} = {val[1]} ")
        return


    def print_by_group(self):
        self._print_by_grouping('groups', self.lookup_by_group)
        return


    def print_by_subgroup(self):
        self._print_by_grouping('subgroups', self.lookup_by_group)
        return


    def rnd_good_emoji(self, qty=1):
        """random good emoji - good is defined in constants
        """
        results = []
        for n in range(qty):
            r = random.randint(1,len(GOOD_EMOJIS))
            key = GOOD_EMOJIS[r-1]
            results.append(self.emoji_data[key])
        return ''.join([x for x in results])


    def rnd_bad_emoji(self, qty=1):
        """random bad emoji - bad is defined in constants
        """
        results = []
        for n in range(qty):
            r = random.randint(1,len(BAD_EMOJIS))
            key = BAD_EMOJIS[r-1]
            results.append(self.emoji_data[key])

        return ''.join([x for x in results])


x = EZEmoji()
x.print_by_group()
