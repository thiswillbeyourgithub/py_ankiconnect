
# py_ankiconnect
Minimal wrapper to simplify the usage of the **awesome** [ankiconnect](https://git.foosoft.net/alex/anki-connect) anki addon.
I made this in about an hour to make it easy to interact with [anki](https://ankitects.github.io/) from my many python projects (see my other repos), as well as from the command line.

# Installation
* `python -m pip install py-ankiconnect` or git clone followed by `python -m pip install -e .`

# How To
## Using the command line
* You can either call it using `py_ankiconnect` or `python -m py_ankiconnect`.
* To see the help: `py_ankiconnect --help` (this will either print it using `rich` if installed or using the pager.)
* Examples:
    * Get the list of tags: `py_ankiconnect getTags | jq`
    * Get info about [Clozolkor](https://github.com/thiswillbeyourgithub/Clozolkor): `py_ankiconnect findModelsByName --modelNames ["Clozolkor"] | jq`
    * You can even use pipes: `py_ankiconnect findNotes --query '*test*' | jq -c '.[0:10]' | py_ankiconnect notesInfo --notes -` (you have to use '-', if will be replaced by the content of sys.stdin)

## Using python
``` python
from py_ankiconnect import PyAnkiconnect
akc = PyAnkiconnect()
# ^ You can set a different port or host there directly:
# akc = PyAnkiconnect(default_port=your_port)

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

# It supposedly even supports async, but this is untested.
import asyncio
akc = PyAnkiconnect(async_mode=True)
async def main():
    return await akc("getTags")
asyncio.run(main())

```
