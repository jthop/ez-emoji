# -*- coding: utf-8 -*-
"""
"""

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import json
import re
import sys
import urllib.request

__version__ = '0.1.8+build.79'


#http://kt.ijs.si/data/Emoji_sentiment_ranking/

########################
#
#   Emoji class
#
########################


class Emoji(object):

    NEGATIVE_SUBS = ['face-unwell', 'face-concerned', 'face-negative']
    POSITIVE_SUBS = ['face-smiling', 'face-affection', 'face-tongue']
    NEUTRAL_SUBS = ['face-neutral-skeptic']
    NEGATIVE = []
    POSITIVE = []
    NEUTRAL = []

    def __init__(self):
        self.short_name = None
        self.name = None
        self.emoji = None
        self.code_point_str = None
        self.status = None
        self.version = None
        self.annotations = []
        self.group = None
        self.subgroup = None
        self.sentiment = None
        self.errors = []

    @property
    def emoji_chr_list(self):
        """ codepoint string to chr
        """
        str_codes = self.code_point_str.split(' ')
        chr_list = [ chr(int(x, 16)) for x in str_codes ]

        return chr_list

    @property
    def as_dict(self):
        d = dict(
            short_name = self.short_name,
            name = self.name,
            emoji = self.emoji,
            status = self.status,
            version = self.version,
            code_point_str = self.code_point_str,
            annotations = self.annotations,
            group = self.group,
            subgroup = self.subgroup,
            sentiment = self.sentiment
        )

        # Add errors field only if needed
        if len(self.errors) > 0:
            d['errors'] = self.errors
        return d

    def save(self):
        """
        """
        #self._calc_sentiment()
        self._verify_integrity()

    def _calc_sentiment(self):
        """
        For now primarily a placeholder until we can utilize some
        real emoji sentiment data.
        """

        if emoji in EmojiDownloader.NEGATIVE or \
            self.subgroup in EmojiDownloader.NEGATIVE_SUBS:
            self.sentiment = '-'
        elif emoji in EmojiDownloader.POSITIVE or \
            self.subgroup in EmojiDownloader.POSITIVE_SUBS:
            self.sentiment = '+'
        elif emoji in EmojiDownloader.NEUTRAL or \
            self.subgroup in EmojiDownloader.NEUTRAL_SUBS:
            self.sentiment = '='
        return

    def _verify_integrity(self):
        # Basic length of emoji vs calculated chr list
        if len(self.emoji) != len(self.emoji_chr_list):
            self.errors.append('BAD-EMOJI-LENGTH')

        # Break the emoji into parts, get the ints, rejoin,
        # then compare that with the original string from unicode
        v = ' '.join([f'{ord(c):04X}' for c in self.emoji])
        if v != self.code_point_str:
            self.errors.append('CODEPOINT-REPRODUCTION-ERROR')

        if len(self.annotations) == 0:
            self.errors.append('CLDR-FAILED')
        return


########################
#
#   Emoji Downloader
#
########################


class EmojiDownloader(object):
    """
    Download the latest emoji data from unicode organization as well as the latest
    CLDR for up to date short_names and annotations.  After parsing all the data the
    emojis are persisted in 2 different forms to a directory you specify via the
    cli args.

    Format 1 - txt_file.   <emoji>=<short_name>:<group>:<subgroup>

    Format 2 - json_file.

    json obj =  {
        'generated': datetime.datetime,
        'generator_version': str,
        'unicode_version': str,
        'groups': list,
        'subgroups': dict,
        'emojis': {
            'short_name': str, 
            'annotations': list,
            'codept_str': str,
            'codept_chr_list': list,
            'subgroup': str, 
            'group': str, 
            'status': str,
            'sentiment': chr
        }
    }

    """

    # class variables used for config
    UNICODE_DATA = 'https://www.unicode.org/Public/emoji/latest/emoji-test.txt'
    CLDR_EN_ANNOTATIONS = 'https://raw.githubusercontent.com/unicode-org/cldr-json/main/' \
'cldr-json/cldr-annotations-full/annotations/en/annotations.json'
    GIT_EMOJI_URL = 'https://api.github.com/emojis'
    TXT_FILE = 'EZEMOJI_UNICODE.txt'
    JSON_FILE = 'EZEMOJI_UNICODE.json'
    GIT_FILE = 'EZEMOJI_GITHUB.md'


    def __init__(self, args):
        """ """
        # initialize instance vars
        self.unicode_version = None
        self.txt_file = None
        self.json_file = None
        self.group = ''
        self.subgroup = ''
        self.subgroups = {}
        self.emojis = []
        self.cldr = {}
        self.dir = './'

        # args via cli
        if args:
            self.dir = args[0]
        self.txt_file = Path(self.dir, EmojiDownloader.TXT_FILE)
        self.json_file = Path(self.dir, EmojiDownloader.JSON_FILE)
        self.git_file = Path(self.dir, EmojiDownloader.GIT_FILE)
        
        # compile regex
        emoji_line = r'(?P<code>.*);\s+(?P<qualification>.*)\s+#(?P<emoji>.*)\s+(?P<ver>E\d+.\d+)\s+(?P<name>.*)'
        self.compiled = re.compile(emoji_line)

        # fetch cldr json data
        cldr = self.fetch_json(EmojiDownloader.CLDR_EN_ANNOTATIONS)
        self.cldr = cldr.get('annotations').get('annotations')

        # fetch unicode org. txt file
        self.test_data = self.fetch_url(EmojiDownloader.UNICODE_DATA, lines=True)

        # fetch git emoji json
        self.git = self.fetch_json(EmojiDownloader.GIT_EMOJI_URL)

        # run main loop
        self.process_unicode()
        self.process_git()
        return

    def fetch_url(self, url, lines=False):
        """Fetch URL with only urllib.  No requests dependancy.
        """
        response = urllib.request.urlopen(url)
        
        # Convert bytes to string type and string type to dict
        string = response.read().decode('utf-8')

        if lines:
            lines = string.splitlines(True)
            return lines
        return string

    def fetch_json(self, url):
        """Fetch json with only urllib.  No requests dependancy.
        """
        request = urllib.request.urlopen(url)
        if(request.getcode()!=200):
            raise ValueError(f'Status code {request.getcode()} returned.')

        data = json.load(request)
        return data

    def lookup_cldr(self, emoji):
        """ """
        a = self.cldr.get(emoji, {})
        annotations = a.get('default', [])
        short_name = a.get('tts', [None])

        c = SimpleNamespace(
            annotations = annotations,
            short_name = short_name[0]
        )
        return c

    def normalize_name(self, s):
        """ Not necessary since we have CLDR, but
        it needs to happy for a number of reasons.
        """
        s = s.replace('flag: ', '') \
               .replace(':', '') \
               .replace(',', '') \
               .replace(u'\u201c', '') \
               .replace(u'\u201d', '') \
               .replace(u'\u229b', '') \
               .strip()
        return s

    def normalize_group(self, s):
        """ Same as above, although Smileys & Emotion
        was really starting to bug me
        """
        s = s.strip('\n') \
        .strip() \
        .replace(' & ', '_') \
        .replace('-', '_') \
        .replace(' ', '_') \
        .lower()
        return s

    def finalize(self):
        """Finish it up.  Format the dict, write to disk, goodbye.
        """
        data = {
            'generated': datetime.today().strftime("%m-%d-%Y"),
            'generator_version': __version__,
            'unicode_version': self.unicode_version,
            'groups': [x for x in self.subgroups.keys()],
            'subgroups': self.subgroups,
            'emojis': {emoji.short_name: emoji.as_dict for emoji in self.emojis}
        }

        with self.txt_file.open('w', encoding='utf-8') as f:
            # First line as a comment to briefly describe the format
            f.write("# EMOJI = GROUP:SUBGROUP:NAME\n")

            for emoji in self.emojis:
                f.write(f"{emoji.emoji} = {emoji.group}:{emoji.subgroup}:{emoji.short_name}\n")

        with self.json_file.open('w', encoding='utf-8') as f:
            json.dump(data, f)

        print(f'Found {len(self.emojis)} emojis.  Unicode Version: {self.unicode_version}.')
        return

    def process_unicode(self):
        """Main loop
        """
        for line in self.test_data:
            match = self.compiled.search(line)

            if line.startswith('# group:'):
                self.group = self.normalize_group(line.split(':')[1])
                self.subgroups[self.group] = []
         
            elif line.startswith('# subgroup:'):
                self.subgroup = self.normalize_group(line.split(':')[1])
                self.subgroups[self.group].append(self.subgroup)

            elif line.startswith('# Version:'):
                self.unicode_version = line.split(':')[1].strip()

            elif self.group == 'component':
                continue

            elif match:
                if 'skin tone' in match.group('name'):
                    continue

                e = Emoji()
                e.name = self.normalize_name(match.group('name'))
                e.emoji = match.group('emoji').strip()
                e.code_point_str = match.group('code').strip()
                e.status = match.group('qualification').strip()
                e.version = match.group('ver').strip()

                _cldr = self.lookup_cldr(e.emoji)
                e.annotations = _cldr.annotations
                e.short_name = _cldr.short_name or e.name
                e.group = self.group
                e.subgroup = self.subgroup

                e.save()
                self.emojis.append(e)

        self.finalize()
        return

    def process_git(self):
        with self.git_file.open('w') as f:
            f.write('# Markdown emojis at Github :wave:\n\n')
            f.write('The following emojis are available in github markdown files. \n\n')
            f.write('Simply add a ":" before and after the tag name which ')
            f.write('represents the emoji you desire.\n\n')
            f.write('| Markdown | Emoji |\n')
            f.write('| ------------- | ------------- |\n')

            for k,v in self.git.items():
                f.write(f'| `:{k}:` | :{k}: |\n')
                image = v


if __name__ == "__main__":
    EmojiDownloader(sys.argv[1:])
