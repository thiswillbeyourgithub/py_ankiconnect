
# py_ankiconnect
Just a simple wrapper to make it simple to use ankiconnect from python or from the commandline. I made this in about an hour to make it easy to interact with anki from my many python projects, as well as from the command line.

# Installation
* `python -m pip install pyankiconnect` or git clone followed by `python -m pip install -e .`

# How To
## Using the command line
* You can either call it using `py_ankiconnect` or `python -m py_ankiconnect`.
* To see the help: `py_ankiconnect --help` (this will either print it using `rich` if installed or using the pager.)
* Examples:
    * Get the list of tags: `py_ankiconnect getTags | jq`
    * Get info about [Clozolkor](https://github.com/thiswillbeyourgithub/Clozolkor): `py_ankiconnect findModelsByName --modelNames ["Clozolkor"] | jq`

## Using python
``` python
from py_ankiconnect import PyAnkiconnect
akc = PyAnkiconnect()
# ^ You can set a different port or host there directly:
# akc = PyAnkiconnect(port=your_port)

# trigger a sync:
result = akc("sync")

# Get the list of all tags:
result = akc("getTags")

# Do some more advanced stuff:
akc(
    action="changeDeck",
    params={
        "cards": [
            1502098034045,
            1502098034048,
            1502298033753
            ],
        "deck": "Japanese::JLPT N3"
        },
)

```
