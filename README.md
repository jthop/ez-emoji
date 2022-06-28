[![Whos your daddy](https://img.shields.io/badge/whos%20your%20daddy-2.0.7rc3-brightgreen.svg)](https://14.do/)
[![works badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.2.0/badge.svg)](https://github.com/nikku/works-on-my-machine)

# ez-emoji  :wave:

We have some emoji data for you.  You can grab standard unicode emojis, in txt or json format above.  Also we maintain the a current set of the github markdown emojis.

## Fresh data  :tada:

Fresh emoji data is always availabe here in the repository's root directory.  

| File | Description |
-------| ----------
[EZEMOJI_UNICODE.txt](https://github.com/jthop/ez-emoji/blob/master/EZEMOJI_UNICODE.txt) | A simple txt file definition of each emoji.  This could easily be adapted to any language.
[EZEMOJI_UNICODE.json](https://github.com/jthop/ez-emoji/blob/master/EZEMOJI_UNICODE.json) | This is a more detailed format using json with the structure illustrated below.
[EZEMOJI_GITHUB.md](https://github.com/jthop/ez-emoji/blob/master/EZEMOJI_GITHUB.md)  |  This is list of all the github markdown emojis, updated via Github's API.
-----------------

```json
{
    "generated": 1656354239,
    "generator_version": "0.1.3+build.83",
    "unicode_version": "14.0",
    "groups": ["smileys_emotion", "people_body", "component", "animals_nature"],
    "subgroups": {"smileys_emotion": ["face-smiling", "face-affection", "face-tongue", "face-hand"]},
    "emojis": {
      "grinning face": {
        "emoji": "\ud83d\ude00",
        "name": "grinning face", 
        "annotations": ["face", "grin", "grinning face"],
        "code_point_str": "1F600",
        "subgroup": "face-smiling", 
        "group": "smileys_emotion", 
        "status": "fully qualified",
        "version": "1.0",
        "sentiment": "+",
        "errors": [],
    }
}
```

## Install your own copy  :floppy_disk:

Github Actions is generating our data here via cron once a week, on Saturday night.  However, if you prefer, go ahead and use [downloader.py](https://github.com/jthop/ez-emoji/blob/master/ez_emoji/downloader.py) to download your own emoji data whenever you desire.


```shell
python downloader.py [optional_destination_directory]
```
_Unicode seems to release major version updates about once per year.  They also do some minor updates in between._

## Use  :muscle:

Download and use our data, or download the entire package.  We have a few utilities as well which are a work in progress.  One is a python Log Formatter which uses emojis.  That utility also utilizes another which simply picks random emojis based on the sentiment desired.
