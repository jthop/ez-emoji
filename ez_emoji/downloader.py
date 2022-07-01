# -*- coding: utf-8 -*-
"""
Google source: https://github.com/googlefonts/noto-emoji/tree/main/png/

SVG!
Twitter source: https://github.com/twitter/twemoji/tree/master/assets/svg
format codepoint.lower().svg or codepoint.lower()[0]-codepoint.lower()[1].svg

"""

from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
import json
import re
import sys
import urllib.request
from curation import POSITIVE
from curation import NEGATIVE

__version__ = '0.1.13+build.86'


#http://kt.ijs.si/data/Emoji_sentiment_ranking/


########################
#
#   Exceptions
#
########################


class EZEmojiException(Exception):
    def __init__(self):
        pass

class FullyQualifiedVariant(EZEmojiException):
    msg = "Variant using the FEOF modifier"
    code = "10"


########################
#
#   Emoji class
#
########################


class Emoji(object):

    NEGATIVE_WORDS = ['confused', 'disappointed',
        'unsure', 'skeptical', 'worried', 'evil',
        'frowning', 'angry'
    ]

    POSITIVE_WORDS = ['juggling', 'tuxedo',
        'smile', 'prayer', 'handshake', 'hang loose',
        'rock-on', 'ILY'
    ]

    """
    variation = [FE00, FE01, FE02, FE03, FE04, FE05, FE06,
        FE07, FE08, FE09, FE0A, FE0B, FE0C, FE0D, FE0E, FE0F]
    and
    U+E0100 to U+E01EF

    str = str.replaceAll("[\\p{C}\\p{So}\uFE00-\uFE0F\\x{E0100}-\\x{E01EF}]+", "")
         .replaceAll(" {2,}", " ")
    """

    def __init__(self):
        self.short_name = None
        self.name = None
        self.emoji = None
        self.code_point_str = None
        self.status = None
        self.emoji_version = None
        self.annotations = []
        self.group = None
        self.subgroup = None
        self.github = None
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
            emoji_version = self.emoji_version,
            code_point_str = self.code_point_str,
            annotations = self.annotations,
            group = self.group,
            subgroup = self.subgroup,
            github = self.github,
            sentiment = self.sentiment,
        )
        if self.errors:
            d['errors'] = self.errors
        return d

    @property
    def positive(self):
        if self.sentiment is not None:
            if self.sentiment == '+':
                return True
        return False

    @property
    def negative(self):
        if self.sentiment is not None:
            if self.sentiment == '-':
                return True
        return False

    @property
    def neutral(self):
        if self.sentiment is not None:
            if self.sentiment == '=':
                return True
        return False

    @property
    def clean_name(self):
        name = self.name
        if name is None:
            name = self.name
        name = name.replace(' ', '_').lower()
        return name

    def save(self):
        """
        """
        if self.short_name is None:
            self.short_name = self.name
            self.errors.append('NO-CLDR')

        """ We need to skip these fully-qualified versions
        with the FE0F modifier or even FE0E.  If not there
        will be 2 emojis with the same name.  Which one we
        should keep I am not 100% on.
        """
        if 'FE0F' in self.code_point_str:
            raise FullyQualifiedVariant()

        self._calc_sentiment()
        self._verify_integrity()
        return True

    def _calc_sentiment(self):
        """
        For now primarily a placeholder until we can utilize some
        real emoji sentiment data.
        """

        if self.short_name in POSITIVE:
            self.sentiment = '+'
        elif self.short_name in NEGATIVE:
            self.sentiment = '-'
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

        if self.name != self.short_name:
            self.errors.append('NAME-SHORT_NAME-MISMATCH')

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
    SENTIMENT_FILE = 'EMOJI_SENTIMENT.json'
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
        self.git = {}
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

        # Run git first so we can attempt to reference git keys
        self.process_git()
        # run main loop
        self.process_unicode()

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
            short_name = short_name[0],
        )
        return c

    def normalize_name(self, s):
        """ Not necessary since we have CLDR, but
        it needs to happy for a number of reasons.
        """

        s = s.replace('flag: ', '') \
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
            .replace('&', 'and') \
            .lower()
        return s

    def finalize(self):
        """Finish it up.  Format the dict, write to disk, goodbye.
        """

        # Make a list of postive and negative emojis
        positives = []
        negatives = []
        for emoji in self.emojis:
            if emoji.positive:
                positives.append(emoji.emoji)
            elif emoji.negative:
                negatives.append(emoji.emoji)
        positives_str = ', '.join([f"'{e}'" for e in positives])
        negatives_str = ', '.join([f"'{e}'" for e in negatives])

        # Generate metadata for the json file
        data = dict(
            generated = datetime.today().strftime("%m-%d-%Y"),
            __version__ = __version__,
            unicode_version = self.unicode_version,
            emoji_quantity = len(self.emojis),
            groups = [x for x in self.subgroups.keys()],
            subgroups = self.subgroups,
            positives = positives_str,
            negatives = negatives_str,
            emojis = {emoji.short_name: emoji.as_dict for emoji in self.emojis}
        )

        # Write the text file
        with self.txt_file.open('w', encoding='utf-8') as f:
            # First line as a comment to briefly describe the format
            f.write("# EMOJI = GROUP:SUBGROUP:NAME\n")
            for emoji in self.emojis:
                f.write(f"{emoji.emoji} = {emoji.group}:{emoji.subgroup}:{emoji.short_name}\n")

            f.write('\n\n')
            f.write(f'POSITIVES = [{positives_str}]\n\n')
            f.write(f'NEGATIVES = [{negatives_str}]\n')

        # Write the json file
        with self.json_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

        # That's all, write a little message to the user
        print(f'Found {len(self.emojis)} emojis.  Unicode Version: {self.unicode_version}.')
        return

    def process_unicode(self):
        """Main loop
        """
        git_lookup = {v: k for k,v in self.git.items()}

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
                e.emoji_version = match.group('ver').strip()

                _cldr = self.lookup_cldr(e.emoji)
                e.annotations = _cldr.annotations
                e.short_name = _cldr.short_name
                e.group = self.group
                e.subgroup = self.subgroup
                if git_lookup.get(e.code_point_str):
                    e.github = git_lookup.get(e.code_point_str)

                try:
                    e.save()
                    self.emojis.append(e)
                except FullyQualifiedVariant:
                    pass

        self.finalize()
        return

    def process_git(self):
        # Git regex
        re_str = r'githubassets.com/images/icons/emoji/(?P<genuine>unicode/)?(?P<cp>.*).png'
        compiled = re.compile(re_str)

        # fetch git emoji json
        git = self.fetch_json(EmojiDownloader.GIT_EMOJI_URL)

        for k,v in git.items():
            match = compiled.search(v)
            if match:
                if not match.group('genuine'):
                    self.git[k] = 'MISSING'
                else:
                    cp = match.group('cp').strip()
                    cp = cp.upper().replace('-', ' ')
                    self.git[k] = cp
            else:
                self.git[k] = v

        with self.git_file.open('w') as f:
            f.write('# Markdown emojis at Github :wave:\n\n')
            f.write('The following emojis are available in github markdown files. \n\n')
            f.write('Simply add a ":" before and after the tag name which ')
            f.write('represents the emoji you desire.\n\n')
            f.write('| Markdown | Emoji | Codepoint | \n')
            f.write('| --------- | --------- | --------- |\n')

            for k,v in self.git.items():
                f.write(f'| `:{k}:` | :{k}: | {v} | \n')


if __name__ == "__main__":
    EmojiDownloader(sys.argv[1:])
