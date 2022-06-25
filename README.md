[![Whos your daddy](https://img.shields.io/badge/whos%20your%20daddy-2.0.7rc3-brightgreen.svg)](https://14.do/)
[![works badge](https://cdn.jsdelivr.net/gh/nikku/works-on-my-machine@v0.2.0/badge.svg)](https://github.com/nikku/works-on-my-machine)


# ez-emoji  	:raising_hand_man:

any deploy/build task you ask of it, the response is always: ican

```
can you bump my version to the next prerelease?
dev@macbook:~/proj$ ican 

can you use that version as a git tag and push a commit to the tag?
dev@macbook:~/proj$ ican 

can you deploy my new version by building a docker container and starting it?
dev@macbook:~/proj$ ican 
```

## Install  :floppy_disk:

Install the ican package via pypi

```shell
pip install ez-emoji
```

## Use  :muscle:

Download the latest emoji data with the emoji_download command

```shell
emoji_download
2 Files created.
```

The command will create the files emoji_data_YYYY_MM_DD.py and emoji_data_YYYY_MM_DD.json.  Use the one that best suits your development environment.


