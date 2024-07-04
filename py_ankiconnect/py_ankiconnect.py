from typing import Union, List, Dict
import json
import urllib.request
from  urllib.error import URLError

class PyAnkiconnect:
    VERSION: str = "0.0.1"

    def __init__(
        self,
        default_host: str = "http://localhost",
        default_port: int = 8765,
        output_json: bool = True,
        ) -> None:
        """
        Params:
        -------
        TODO

        """
        self.host: str = default_host
        self.port: int = default_port
        self.output_json: bool = output_json

    def call(
        self,
        action: str,
        **params,
        ) -> Union[List, str]:
        """
        Params:
        -------
        - action: str, for example 'sync'
        - params: dict, any parameters supported by the action.
            * With addition of "port", "host" and "output_json" which,
              if specified will overide (for this call only) the value
              given at instanciation time.


        Example:
        --------
        instance = PyAnkiconnect(
            host="http://localhost",
            port=8765,
            output_json=True
        )
        instance.call(
            action="changeDeck",
            params={
                "cards": [
                    1502098034045,
                    1502098034048,
                    1502298033753
                    ],
                "deck": "Japanese::JLPT N3"
                },
                output_json=False,  # <- changed only for this call!
        )
        """

        if "host" in params:
            host = params["host"]
            del params["host"]
        else:
            host = self.host
        if "port" in params:
            port = params["port"]
            del params["port"]
        else:
            port = self.port
        address: str = f"{host}:{port}"

        requestJson: bytes = json.dumps(
            {
                'action': action,
                'params': params,
                'version': 6
            }
        ).encode('utf-8')

        try:
            response: Dict = json.load(
                urllib.request.urlopen(
                    urllib.request.Request(
                        address,
                        requestJson
                    )
                )
            )
        except (ConnectionRefusedError, URLError) as e:
            raise Exception(
                f"Error: '{str(e)}': is Anki open? is ankiconnect enabled? "
                f"is your firewall configured? Adress is '{address}'"
            )

        if len(response) != 2:
            raise Exception(
                'Response has an unexpected number of fields: '
                f'{len(response)}, expected 2'
            )
        if 'error' not in response:
            raise Exception(
                f'Response is missing the "error" field: "{response}"')
        if 'result' not in response:
            raise Exception(
                f'Response is missing the "result" field: "{response}"')
        if response['error'] is not None:
            raise Exception(f"Received error: '{response['error']}'")

        if self.output_json:
            return json.dumps(response['result'])
        else:
            return response['result']


# set the docstring
docstring = """
# This docstring is simply a copy from the AnkiConnect readme from jully 2024. It is put as docstring for convenience but do checkout [the official AnkiConnect documentation](https://github.com/amikey/anki-connect/).




### Supported Actions ###

Below is a comprehensive list of currently supported actions. Note that deprecated APIs will continue to function
despite not being listed on this page as long as your request is labeled with a version number corresponding to when the
API was available for use.

This page currently documents **version 5** of the API. Make sure to include this version number in your requests to
guarantee that your application continues to function properly in the future.

#### Miscellaneous ####

*   **version**

    Gets the version of the API exposed by this plugin. Currently versions `1` through `5` are defined.

    This should be the first call you make to make sure that your application and AnkiConnect are able to communicate
    properly with each other. New versions of AnkiConnect are backwards compatible; as long as you are using actions
    which are available in the reported AnkiConnect version or earlier, everything should work fine.

    *Sample request*:
    ```json
    {
        "action": "version",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": 5,
        "error": null
    }
    ```

*   **upgrade**

    Displays a confirmation dialog box in Anki asking the user if they wish to upgrade AnkiConnect to the latest version
    from the project's [master branch](https://raw.githubusercontent.com/FooSoft/anki-connect/master/AnkiConnect.py) on
    GitHub. Returns a boolean value indicating if the plugin was upgraded or not.

    *Sample request*:
    ```json
    {
        "action": "upgrade",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **multi**

    Performs multiple actions in one request, returning an array with the response of each action (in the given order).

    *Sample request*:
    ```json
    {
        "action": "multi",
        "version": 5,
        "params": {
            "actions": [
                {"action": "deckNames"},
                {
                    "action": "browse",
                    "params": {"query": "deck:current"}
                }
            ]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [
            ["Default"],
            [1494723142483, 1494703460437, 1494703479525]
        ],
        "error": null
    }
    ```

#### Decks ####

*   **deckNames**

    Gets the complete list of deck names for the current user.

    *Sample request*:
    ```json
    {
        "action": "deckNames",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": ["Default"],
        "error": null
    }
    ```

*   **deckNamesAndIds**

    Gets the complete list of deck names and their respective IDs for the current user.

    *Sample request*:
    ```json
    {
        "action": "deckNamesAndIds",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {"Default": 1},
        "error": null
    }
    ```

*   **getDecks**

    Accepts an array of card IDs and returns an object with each deck name as a key, and its value an array of the given
    cards which belong to it.

    *Sample request*:
    ```json
    {
        "action": "getDecks",
        "version": 5,
        "params": {
            "cards": [1502298036657, 1502298033753, 1502032366472]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {
            "Default": [1502032366472],
            "Japanese::JLPT N3": [1502298036657, 1502298033753]
        },
        "error": null
    }
    ```

*   **changeDeck**

    Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet.

    *Sample request*:
    ```json
    {
        "action": "changeDeck",
        "version": 5,
        "params": {
            "cards": [1502098034045, 1502098034048, 1502298033753],
            "deck": "Japanese::JLPT N3"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **deleteDecks**

    Deletes decks with the given names. If `cardsToo` is `true` (defaults to `false` if unspecified), the cards within
    the deleted decks will also be deleted; otherwise they will be moved to the default deck.

    *Sample request*:
    ```json
    {
        "action": "deleteDecks",
        "version": 5,
        "params": {
            "decks": ["Japanese::JLPT N5", "Easy Spanish"],
            "cardsToo": true
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **getDeckConfig**

    Gets the configuration group object for the given deck.

    *Sample request*:
    ```json
    {
        "action": "getDeckConfig",
        "version": 5,
        "params": {
            "deck": "Default"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {
            "lapse": {
                "leechFails": 8,
                "delays": [10],
                "minInt": 1,
                "leechAction": 0,
                "mult": 0
            },
            "dyn": false,
            "autoplay": true,
            "mod": 1502970872,
            "id": 1,
            "maxTaken": 60,
            "new": {
                "bury": true,
                "order": 1,
                "initialFactor": 2500,
                "perDay": 20,
                "delays": [1, 10],
                "separate": true,
                "ints": [1, 4, 7]
            },
            "name": "Default",
            "rev": {
                "bury": true,
                "ivlFct": 1,
                "ease4": 1.3,
                "maxIvl": 36500,
                "perDay": 100,
                "minSpace": 1,
                "fuzz": 0.05
            },
            "timer": 0,
            "replayq": true,
            "usn": -1
        },
        "error": null
    }
    ```

*   **saveDeckConfig**

    Saves the given configuration group, returning `true` on success or `false` if the ID of the configuration group is
    invalid (such as when it does not exist).

    *Sample request*:
    ```json
    {
        "action": "saveDeckConfig",
        "version": 5,
        "params": {
            "config": {
                "lapse": {
                    "leechFails": 8,
                    "delays": [10],
                    "minInt": 1,
                    "leechAction": 0,
                    "mult": 0
                },
                "dyn": false,
                "autoplay": true,
                "mod": 1502970872,
                "id": 1,
                "maxTaken": 60,
                "new": {
                    "bury": true,
                    "order": 1,
                    "initialFactor": 2500,
                    "perDay": 20,
                    "delays": [1, 10],
                    "separate": true,
                    "ints": [1, 4, 7]
                },
                "name": "Default",
                "rev": {
                    "bury": true,
                    "ivlFct": 1,
                    "ease4": 1.3,
                    "maxIvl": 36500,
                    "perDay": 100,
                    "minSpace": 1,
                    "fuzz": 0.05
                },
                "timer": 0,
                "replayq": true,
                "usn": -1
            }
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **setDeckConfigId**

    Changes the configuration group for the given decks to the one with the given ID. Returns `true` on success or
    `false` if the given configuration group or any of the given decks do not exist.

    *Sample request*:
    ```json
    {
        "action": "setDeckConfigId",
        "version": 5,
        "params": {
            "decks": ["Default"],
            "configId": 1
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **cloneDeckConfigId**

    Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default
    group if this is unspecified. Returns the ID of the new configuration group, or `false` if the specified group to
    clone from does not exist.

    *Sample request*:
    ```json
    {
        "action": "cloneDeckConfigId",
        "version": 5,
        "params": {
            "name": "Copy of Default",
            "cloneFrom": 1
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": 1502972374573,
        "error": null
    }
    ```

*   **removeDeckConfigId**

    Removes the configuration group with the given ID, returning `true` if successful, or `false` if attempting to
    remove either the default configuration group (ID = 1) or a configuration group that does not exist.

    *Sample request*:
    ```json
    {
        "action": "removeDeckConfigId",
        "version": 5,
        "params": {
            "configId": 1502972374573
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

#### Models ####

*   **modelNames**

    Gets the complete list of model names for the current user.

    *Sample request*:
    ```json
    {
        "action": "modelNames",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": ["Basic", "Basic (and reversed card)"],
        "error": null
    }
    ```

*   **modelNamesAndIds**

    Gets the complete list of model names and their corresponding IDs for the current user.

    *Sample request*:
    ```json
    {
        "action": "modelNamesAndIds",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {
            "Basic": 1483883011648,
            "Basic (and reversed card)": 1483883011644,
            "Basic (optional reversed card)": 1483883011631,
            "Cloze": 1483883011630
        },
        "error": null
    }
    ```

*   **modelFieldNames**

    Gets the complete list of field names for the provided model name.

    *Sample request*:
    ```json
    {
        "action": "modelFieldNames",
        "version": 5,
        "params": {
            "modelName": "Basic"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": ["Front", "Back"],
        "error": null
    }
    ```

*   **modelFieldsOnTemplates**

    Returns an object indicating the fields on the question and answer side of each card template for the given model
    name. The question side is given first in each array.

    *Sample request*:
    ```json
    {
        "action": "modelFieldsOnTemplates",
        "version": 5,
        "params": {
            "modelName": "Basic (and reversed card)"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {
            "Card 1": [["Front"], ["Back"]],
            "Card 2": [["Back"], ["Front"]]
        },
        "error": null
    }
    ```

#### Notes ####

*   **addNote**

    Creates a note using the given deck and model, with the provided field values and tags. Returns the identifier of
    the created note created on success, and `null` on failure.

    AnkiConnect can download audio files and embed them in newly created notes. The corresponding `audio` note member is
    optional and can be omitted. If you choose to include it, the `url` and `filename` fields must be also defined. The
    `skipHash` field can be optionally provided to skip the inclusion of downloaded files with an MD5 hash that matches
    the provided value. This is useful for avoiding the saving of error pages and stub files. The `fields` member is a
    list of fields that should play audio when the card is displayed in Anki.

    *Sample request*:
    ```json
    {
        "action": "addNote",
        "version": 5,
        "params": {
            "note": {
                "deckName": "Default",
                "modelName": "Basic",
                "fields": {
                    "Front": "front content",
                    "Back": "back content"
                },
                "tags": [
                    "yomichan"
                ],
                "audio": {
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": "Front"
                }
            }
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": 1496198395707,
        "error": null
    }
    ```

*   **addNotes**

    Creates multiple notes using the given deck and model, with the provided field values and tags. Returns an array of
    identifiers of the created notes (notes that could not be created will have a `null` identifier). Please see the
    documentation for `addNote` for an explanation of objects in the `notes` array.

    *Sample request*:
    ```json
    {
        "action": "addNotes",
        "version": 5,
        "params": {
            "notes": [
                {
                    "deckName": "Default",
                    "modelName": "Basic",
                    "fields": {
                        "Front": "front content",
                        "Back": "back content"
                    },
                    "tags": [
                        "yomichan"
                    ],
                    "audio": {
                        "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                        "filename": "yomichan_ねこ_猫.mp3",
                        "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                        "fields": "Front"
                    }
                }
            ]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [1496198395707, null],
        "error": null
    }
    ```

*   **canAddNotes**

    Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of
    booleans indicating whether or not the parameters at the corresponding index could be used to create a new note.

    *Sample request*:
    ```json
    {
        "action": "canAddNotes",
        "version": 5,
        "params": {
            "notes": [
                {
                    "deckName": "Default",
                    "modelName": "Basic",
                    "fields": {
                        "Front": "front content",
                        "Back": "back content"
                    },
                    "tags": [
                        "yomichan"
                    ]
                }
            ]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [true],
        "error": null
    }
    ```

*   **updateNoteFields**

    Modify the fields of an exist note.

    *Sample request*:
    ```json
    {
        "action": "updateNoteFields",
        "version": 5,
        "params": {
            "note": {
                "id": 1514547547030,
                "fields": {
                    "Front": "new front content",
                    "Back": "new back content"
                }
            }
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **addTags**

    Adds tags to notes by note ID.

    *Sample request*:
    ```json
    {
        "action": "addTags",
        "version": 5,
        "params": {
            "notes": [1483959289817, 1483959291695],
            "tags": "european-languages"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **removeTags**

    Remove tags from notes by note ID.

    *Sample request*:
    ```json
    {
        "action": "removeTags",
        "version": 5,
        "params": {
            "notes": [1483959289817, 1483959291695],
            "tags": "european-languages"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **getTags**

    Gets the complete list of tags for the current user.

    *Sample request*:
    ```json
    {
        "action": "getTags",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": ["european-languages", "idioms"],
        "error": null
    }
    ```

*   **findNotes**

    Returns an array of note IDs for a given query. Same query syntax as `guiBrowse`.

    *Sample request*:
    ```json
    {
        "action": "findNotes",
        "version": 5,
        "params": {
            "query": "deck:current"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [1483959289817, 1483959291695],
        "error": null
    }
    ```

*   **notesInfo**

    Returns a list of objects containing for each note ID the note fields, tags, note type and the cards belonging to
    the note.

    *Sample request*:
    ```json
    {
        "action": "notesInfo",
        "version": 5,
        "params": {
            "notes": [1502298033753]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [
            {
                "noteId":1502298033753,
                "modelName": "Basic",
                "tags":["tag","another_tag"],
                "fields": {
                    "Front": {"value": "front content", "order": 0},
                    "Back": {"value": "back content", "order": 1}
                }
            }
        ],
        "error": null
    }
    ```


#### Cards ####

*   **suspend**

    Suspend cards by card ID; returns `true` if successful (at least one card wasn't already suspended) or `false`
    otherwise.

    *Sample request*:
    ```json
    {
        "action": "suspend",
        "version": 5,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **unsuspend**

    Unsuspend cards by card ID; returns `true` if successful (at least one card was previously suspended) or `false`
    otherwise.

    *Sample request*:
    ```json
    {
        "action": "unsuspend",
        "version": 5,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **areSuspended**

    Returns an array indicating whether each of the given cards is suspended (in the same order).

    *Sample request*:
    ```json
    {
        "action": "areSuspended",
        "version": 5,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [false, true],
        "error": null
    }
    ```

*   **areDue**

    Returns an array indicating whether each of the given cards is due (in the same order). *Note*: cards in the
    learning queue with a large interval (over 20 minutes) are treated as not due until the time of their interval has
    passed, to match the way Anki treats them when reviewing.

    *Sample request*:
    ```json
    {
        "action": "areDue",
        "version": 5,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [false, true],
        "error": null
    }
    ```

*   **getIntervals**

    Returns an array of the most recent intervals for each given card ID, or a 2-dimensional array of all the intervals
    for each given card ID when `complete` is `true`. Negative intervals are in seconds and positive intervals in days.

    *Sample request 1*:
    ```json
    {
        "action": "getIntervals",
        "version": 5,
        "params": {
            "cards": [1502298033753, 1502298036657]
        }
    }
    ```

    *Sample result 1*:
    ```json
    {
        "result": [-14400, 3],
        "error": null
    }
    ```

    *Sample request 2*:
    ```json
    {
        "action": "getIntervals",
        "version": 5,
        "params": {
            "cards": [1502298033753, 1502298036657],
            "complete": true
        }
    }
    ```

    *Sample result 2*:
    ```json
    {
        "result": [
            [-120, -180, -240, -300, -360, -14400],
            [-120, -180, -240, -300, -360, -14400, 1, 3]
        ],
        "error": null
    }
    ```

*   **findCards**

    Returns an array of card IDs for a given query. Functionally identical to `guiBrowse` but doesn't use the GUI for
    better performance.

    *Sample request*:
    ```json
    {
        "action": "findCards",
        "version": 5,
        "params": {
            "query": "deck:current"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [1494723142483, 1494703460437, 1494703479525],
        "error": null
    }
    ```

*   **cardsToNotes**

    Returns an unordered array of note IDs for the given card IDs. For cards with the same note, the ID is only given
    once in the array.

    *Sample request*:
    ```json
    {
        "action": "cardsToNotes",
        "version": 5,
        "params": {
            "cards": [1502098034045, 1502098034048, 1502298033753]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [1502098029797, 1502298025183],
        "error": null
    }
    ```

*   **cardsInfo**

    Returns a list of objects containing for each card ID the card fields, front and back sides including CSS, note
    type, the note that the card belongs to, and deck name, as well as ease and interval.

    *Sample request*:
    ```json
    {
        "action": "cardsInfo",
        "version": 5,
        "params": {
            "cards": [1498938915662, 1502098034048]
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [
            {
                "answer": "back content",
                "question": "front content",
                "deckName": "Default",
                "modelName": "Basic",
                "fieldOrder": 1,
                "fields": {
                    "Front": {"value": "front content", "order": 0},
                    "Back": {"value": "back content", "order": 1}
                },
                "css":"p {font-family:Arial;}",
                "cardId": 1498938915662,
                "interval": 16,
                "note":1502298033753
            },
            {
                "answer": "back content",
                "question": "front content",
                "deckName": "Default",
                "modelName": "Basic",
                "fieldOrder": 0,
                "fields": {
                    "Front": {"value": "front content", "order": 0},
                    "Back": {"value": "back content", "order": 1}
                },
                "css":"p {font-family:Arial;}",
                "cardId": 1502098034048,
                "interval": 23,
                "note":1502298033753
            }
        ],
        "error": null
    }
    ```

#### Media ####

*   **storeMediaFile**

    Stores a file with the specified base64-encoded contents inside the media folder. To prevent Anki from removing
    files not used by any cards (e.g. for configuration files), prefix the filename with an underscore. These files are
    still synchronized to AnkiWeb.

    *Sample request*:
    ```json
    {
        "action": "storeMediaFile",
        "version": 5,
        "params": {
            "filename": "_hello.txt",
            "data": "SGVsbG8sIHdvcmxkIQ=="
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

    *Content of `_hello.txt`*:
    ```
    Hello world!
    ```

*   **retrieveMediaFile**

    Retrieves the base64-encoded contents of the specified file, returning `false` if the file does not exist.

    *Sample request*:
    ```json
    {
        "action": "retrieveMediaFile",
        "version": 5,
        "params": {
            "filename": "_hello.txt"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": "SGVsbG8sIHdvcmxkIQ==",
        "error": null
    }
    ```

*   **deleteMediaFile**

    Deletes the specified file inside the media folder.

    *Sample request*:
    ```json
    {
        "action": "deleteMediaFile",
        "version": 5,
        "params": {
            "filename": "_hello.txt"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

#### Graphical ####

*   **guiBrowse**

    Invokes the *Card Browser* dialog and searches for a given query. Returns an array of identifiers of the cards that
    were found.

    *Sample request*:
    ```json
    {
        "action": "guiBrowse",
        "version": 5,
        "params": {
            "query": "deck:current"
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": [1494723142483, 1494703460437, 1494703479525],
        "error": null
    }
    ```

*   **guiAddCards**

    Invokes the *Add Cards* dialog.

    *Sample request*:
    ```json
    {
        "action": "guiAddCards",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **guiCurrentCard**

    Returns information about the current card or `null` if not in review mode.

    *Sample request*:
    ```json
    {
        "action": "guiCurrentCard",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": {
            "answer": "back content",
            "question": "front content",
            "deckName": "Default",
            "modelName": "Basic",
            "fieldOrder": 0,
            "fields": {
                "Front": {"value": "front content", "order": 0},
                "Back": {"value": "back content", "order": 1}
            },
            "cardId": 1498938915662,
            "buttons": [1, 2, 3]
        },
        "error": null
    }
    ```

*   **guiStartCardTimer**

    Starts or resets the `timerStarted` value for the current card. This is useful for deferring the start time to when
    it is displayed via the API, allowing the recorded time taken to answer the card to be more accurate when calling
    `guiAnswerCard`.

    *Sample request*:
    ```json
    {
        "action": "guiStartCardTimer",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiShowQuestion**

    Shows question text for the current card; returns `true` if in review mode or `false` otherwise.

    *Sample request*:
    ```json
    {
        "action": "guiShowQuestion",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiShowAnswer**

    Shows answer text for the current card; returns `true` if in review mode or `false` otherwise.

    *Sample request*:
    ```json
    {
        "action": "guiShowAnswer",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiAnswerCard**

    Answers the current card; returns `true` if succeeded or `false` otherwise. Note that the answer for the current
    card must be displayed before before any answer can be accepted by Anki.

    *Sample request*:
    ```json
    {
        "action": "guiAnswerCard",
        "version": 5,
        "params": {
            "ease": 1
        }
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiDeckOverview**

    Opens the *Deck Overview* dialog for the deck with the given name; returns `true` if succeeded or `false` otherwise.

    *Sample request*:
    ```json
    {
        "action": "guiDeckOverview",
        "version": 5,
		"params": {
			"name": "Default"
		}
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiDeckBrowser**

    Opens the *Deck Browser* dialog.

    *Sample request*:
    ```json
    {
        "action": "guiDeckBrowser",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

*   **guiDeckReview**

    Starts review for the deck with the given name; returns `true` if succeeded or `false` otherwise.

    *Sample request*:
    ```json
    {
        "action": "guiDeckReview",
        "version": 5,
		"params": {
			"name": "Default"
		}
    }
    ```

    *Sample result*:
    ```json
    {
        "result": true,
        "error": null
    }
    ```

*   **guiExitAnki**

    Schedules a request to gracefully close Anki. This operation is asynchronous, so it will return immediately and
    won't wait until the Anki process actually terminates.

    *Sample request*:
    ```json
    {
        "action": "guiExitAnki",
        "version": 5
    }
    ```

    *Sample result*:
    ```json
    {
        "result": null,
        "error": null
    }
    ```

## License ##

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
PyAnkiconnect.__doc__ = docstring
