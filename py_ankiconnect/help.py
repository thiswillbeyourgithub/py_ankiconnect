docstring = """
# This docstring below is simply the AnkiConnect README.md from jully 2024. It's here for convenience but do checkout [the official AnkiConnect documentation](https://git.foosoft.net/alex/anki-connect).

## Supported Actions

Documentation for currently supported actions is split up by category and is referenced below. Note that deprecated APIs
will continue to function despite not being listed on this page as long as your request is labeled with a version number
corresponding to when the API was available for use.
Search parameters are passed to Anki, check the docs for more information: https://docs.ankiweb.net/searching.html

* [Card Actions](#card-actions)
* [Deck Actions](#deck-actions)
* [Graphical Actions](#graphical-actions)
* [Media Actions](#media-actions)
* [Miscellaneous Actions](#miscellaneous-actions)
* [Model Actions](#model-actions)
* [Note Actions](#note-actions)
* [Statistic Actions](#statistic-actions)

---

### Card Actions

#### `getEaseFactors`

*   Returns an array with the ease factor for each of the given cards (in the same order).

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getEaseFactors",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [4100, 3900],
        "error": null
    }
    ```
    </details>

#### `setEaseFactors`

*   Sets ease factor of cards by card ID; returns `true` if successful (all cards existed) or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "setEaseFactors",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217],
            "easeFactors": [4100, 3900]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [true, true],
        "error": null
    }
    ```
    </details>


#### `setSpecificValueOfCard`

*   Sets specific value of a single card. Given the risk of wreaking havor in the database when changing some of the values of a card, some of the keys require the argument "warning_check" set to True.
    This can be used to set a card's flag, change it's ease factor, change the review order in a filtered deck and change the column "data" (not currently used by anki apparantly), and many other values.
    A list of values and explanation of their respective utility can be found at [AnkiDroid's wiki](https://github.com/ankidroid/Anki-Android/wiki/Database-Structure).

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "setSpecificValueOfCard",
        "version": 6,
        "params": {
            "card": 1483959291685,
            "keys": ["flags", "odue"],
            "newValues": ["1", "-100"]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [true, true],
        "error": null
    }
    ```
    </details>


#### `suspend`

*   Suspend cards by card ID; returns `true` if successful (at least one card wasn't already suspended) or `false`
    otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "suspend",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `unsuspend`

*   Unsuspend cards by card ID; returns `true` if successful (at least one card was previously suspended) or `false`
    otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "unsuspend",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `suspended`

*   Check if card is suspended by its ID. Returns `true` if suspended, `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "suspended",
        "version": 6,
        "params": {
            "card": 1483959293217
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `areSuspended`

*   Returns an array indicating whether each of the given cards is suspended (in the same order). If card doesn't
    exist returns `null`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "areSuspended",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217, 1234567891234]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [false, true, null],
        "error": null
    }
    ```
    </details>

#### `areDue`

*   Returns an array indicating whether each of the given cards is due (in the same order). *Note*: cards in the
    learning queue with a large interval (over 20 minutes) are treated as not due until the time of their interval has
    passed, to match the way Anki treats them when reviewing.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "areDue",
        "version": 6,
        "params": {
            "cards": [1483959291685, 1483959293217]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [false, true],
        "error": null
    }
    ```
    </details>

#### `getIntervals`

*   Returns an array of the most recent intervals for each given card ID, or a 2-dimensional array of all the intervals
    for each given card ID when `complete` is `true`. Negative intervals are in seconds and positive intervals in days.

    <details>
    <summary><i>Sample request 1:</i></summary>

    ```json
    {
        "action": "getIntervals",
        "version": 6,
        "params": {
            "cards": [1502298033753, 1502298036657]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result 1:</i></summary>

    ```json
    {
        "result": [-14400, 3],
        "error": null
    }
    ```
    </details>

    <details>
    <summary><i>Sample request 2:</i></summary>

    ```json
    {
        "action": "getIntervals",
        "version": 6,
        "params": {
            "cards": [1502298033753, 1502298036657],
            "complete": true
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result 2:</i></summary>

    ```json
    {
        "result": [
            [-120, -180, -240, -300, -360, -14400],
            [-120, -180, -240, -300, -360, -14400, 1, 3]
        ],
        "error": null
    }
    ```
    </details>

#### `findCards`

*   Returns an array of card IDs for a given query. Functionally identical to `guiBrowse` but doesn't use the GUI for
    better performance.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "findCards",
        "version": 6,
        "params": {
            "query": "deck:current"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [1494723142483, 1494703460437, 1494703479525],
        "error": null
    }
    ```
    </details>

#### `cardsToNotes`

*   Returns an unordered array of note IDs for the given card IDs. For cards with the same note, the ID is only given
    once in the array.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "cardsToNotes",
        "version": 6,
        "params": {
            "cards": [1502098034045, 1502098034048, 1502298033753]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [1502098029797, 1502298025183],
        "error": null
    }
    ```
    </details>

#### `cardsModTime`

*   Returns a list of objects containings for each card ID the modification time.
    This function is about 15 times faster than executing `cardsInfo`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "cardsModTime",
        "version": 6,
        "params": {
            "cards": [1498938915662, 1502098034048]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
            {
                "cardId": 1498938915662,
                "mod": 1629454092
            }
        ],
        "error": null
    }
    ```
    </details>


#### `cardsInfo`

*   Returns a list of objects containing for each card ID the card fields, front and back sides including CSS, note
    type, the note that the card belongs to, and deck name, last modification timestamp as well as ease and interval.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "cardsInfo",
        "version": 6,
        "params": {
            "cards": [1498938915662, 1502098034048]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

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
                "note":1502298033753,
                "ord": 1,
                "type": 0,
                "queue": 0,
                "due": 1,
                "reps": 1,
                "lapses": 0,
                "left": 6,
                "mod": 1629454092
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
                "note":1502298033753,
                "ord": 1,
                "type": 0,
                "queue": 0,
                "due": 1,
                "reps": 1,
                "lapses": 0,
                "left": 6
            }
        ],
        "error": null
    }
    ```
    </details>

#### `forgetCards`

*   Forget cards, making the cards new again.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "forgetCards",
        "version": 6,
        "params": {
            "cards": [1498938915662, 1502098034048]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `relearnCards`

*   Make cards be "relearning".

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "relearnCards",
        "version": 6,
        "params": {
            "cards": [1498938915662, 1502098034048]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `answerCards`

*   Answer cards. Ease is between 1 (Again) and 4 (Easy). Will start the timer immediately before answering. Returns `true` if card exists, `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "answerCards",
        "version": 6,
        "params": {
            "answers": [
                {
                    "cardId": 1498938915662,
                    "ease": 2
                },
                {
                    "cardId": 1502098034048,
                    "ease": 4
                }
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [true, true],
        "error": null
    }
    ```
    </details>

---

### Deck Actions

#### `deckNames`

*   Gets the complete list of deck names for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "deckNames",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["Default"],
        "error": null
    }
    ```
    </details>

#### `deckNamesAndIds`

*   Gets the complete list of deck names and their respective IDs for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "deckNamesAndIds",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {"Default": 1},
        "error": null
    }
    ```
    </details>

#### `getDecks`

*   Accepts an array of card IDs and returns an object with each deck name as a key, and its value an array of the given
    cards which belong to it.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getDecks",
        "version": 6,
        "params": {
            "cards": [1502298036657, 1502298033753, 1502032366472]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "Default": [1502032366472],
            "Japanese::JLPT N3": [1502298036657, 1502298033753]
        },
        "error": null
    }
    ```
    </details>

#### `createDeck`

*   Create a new empty deck. Will not overwrite a deck that exists with the same name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "createDeck",
        "version": 6,
        "params": {
            "deck": "Japanese::Tokyo"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1519323742721,
        "error": null
    }
    ```
    </details>

#### `changeDeck`

*   Moves cards with the given IDs to a different deck, creating the deck if it doesn't exist yet.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "changeDeck",
        "version": 6,
        "params": {
            "cards": [1502098034045, 1502098034048, 1502298033753],
            "deck": "Japanese::JLPT N3"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `deleteDecks`

*   Deletes decks with the given names.
    The argument `cardsToo` *must* be specified and set to `true`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "deleteDecks",
        "version": 6,
        "params": {
            "decks": ["Japanese::JLPT N5", "Easy Spanish"],
            "cardsToo": true
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `getDeckConfig`

*   Gets the configuration group object for the given deck.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getDeckConfig",
        "version": 6,
        "params": {
            "deck": "Default"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

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
    </details>

#### `saveDeckConfig`

*   Saves the given configuration group, returning `true` on success or `false` if the ID of the configuration group is
    invalid (such as when it does not exist).

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "saveDeckConfig",
        "version": 6,
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
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `setDeckConfigId`

*   Changes the configuration group for the given decks to the one with the given ID. Returns `true` on success or
    `false` if the given configuration group or any of the given decks do not exist.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "setDeckConfigId",
        "version": 6,
        "params": {
            "decks": ["Default"],
            "configId": 1
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `cloneDeckConfigId`

*   Creates a new configuration group with the given name, cloning from the group with the given ID, or from the default
    group if this is unspecified. Returns the ID of the new configuration group, or `false` if the specified group to
    clone from does not exist.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "cloneDeckConfigId",
        "version": 6,
        "params": {
            "name": "Copy of Default",
            "cloneFrom": 1
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1502972374573,
        "error": null
    }
    ```
    </details>

#### `removeDeckConfigId`

*   Removes the configuration group with the given ID, returning `true` if successful, or `false` if attempting to
    remove either the default configuration group (ID = 1) or a configuration group that does not exist.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "removeDeckConfigId",
        "version": 6,
        "params": {
            "configId": 1502972374573
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `getDeckStats`

*   Gets statistics such as total cards and cards due for the given decks.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getDeckStats",
        "version": 6,
        "params": {
            "decks": ["Japanese::JLPT N5", "Easy Spanish"]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "1651445861967": {
                "deck_id": 1651445861967,
                "name": "Japanese::JLPT N5",
                "new_count": 20,
                "learn_count": 0,
                "review_count": 0,
                "total_in_deck": 1506
            },
            "1651445861960": {
                "deck_id": 1651445861960,
                "name": "Easy Spanish",
                "new_count": 26,
                "learn_count": 10,
                "review_count": 5,
                "total_in_deck": 852
            }
        },
        "error": null
    }
    ```
    </details>

---

### Graphical Actions

#### `guiBrowse`

*   Invokes the *Card Browser* dialog and searches for a given query. Returns an array of identifiers of the cards that
    were found. Query syntax is [documented here](https://docs.ankiweb.net/searching.html).

    Optionally, the `reorderCards` property can be provided to reorder the cards shown in the *Card Browser*.
    This is an array including the `order` and `columnId` objects. `order` can be either `ascending` or `descending` while `columnId` can be one of several column identifiers (as documented in the [Anki source code](https://github.com/ankitects/anki/blob/main/rslib/src/browser_table.rs)).
    The specified column needs to be visible in the *Card Browser*.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiBrowse",
        "version": 6,
        "params": {
            "query": "deck:current",
            "reorderCards": {
                "order": "descending",
                "columnId": "noteCrt"
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [1494723142483, 1494703460437, 1494703479525],
        "error": null
    }
    ```
    </details>

#### `guiSelectNote`

*   Finds the open instance of the *Card Browser* dialog and selects a note given a note identifier.
    Returns `true` if the *Card Browser* is open, `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiSelectNote",
        "version": 6,
        "params": {
            "note": 1494723142483
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiSelectedNotes`

*   Finds the open instance of the *Card Browser* dialog and returns an array of identifiers of the notes that are
    selected. Returns an empty list if the browser is not open.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiSelectedNotes",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [1494723142483, 1494703460437, 1494703479525],
        "error": null
    }
    ```
    </details>

#### `guiAddCards`

*   Invokes the *Add Cards* dialog, presets the note using the given deck and model, with the provided field values and tags.
    Invoking it multiple times closes the old window and _reopen the window_ with the new provided values.

    Audio, video, and picture files can be embedded into the fields via the `audio`, `video`, and `picture` keys, respectively.
    Refer to the documentation of `addNote` and `storeMediaFile` for an explanation of these fields.

    The result is the ID of the note which would be added, if the user chose to confirm the *Add Cards* dialogue.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiAddCards",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Default",
                "modelName": "Cloze",
                "fields": {
                    "Text": "The capital of Romania is {{c1::Bucharest}}",
                    "Extra": "Romania is a country in Europe"
                },
                "tags": [
                  "countries"
                ],
                "picture": [{
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/EU-Romania.svg/285px-EU-Romania.svg.png",
                    "filename": "romania.png",
                    "fields": [
                        "Extra"
                    ]
                }]
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1496198395707,
        "error": null
    }
    ```
    </details>

#### `guiEditNote`

*   Opens the *Edit* dialog with a note corresponding to given note ID.
    The dialog is similar to the *Edit Current* dialog, but:

    * has a Preview button to preview the cards for the note
    * has a Browse button to open the browser with these cards
    * has Previous/Back buttons to navigate the history of the dialog
    * has no bar with the Close button

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiEditNote",
        "version": 6,
        "params": {
            "note": 1649198355435
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `guiCurrentCard`

*   Returns information about the current card or `null` if not in review mode.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiCurrentCard",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

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
            "template": "Forward",
            "cardId": 1498938915662,
            "buttons": [1, 2, 3],
            "nextReviews": ["<1m", "<10m", "4d"]
        },
        "error": null
    }
    ```
    </details>

#### `guiStartCardTimer`

*   Starts or resets the `timerStarted` value for the current card. This is useful for deferring the start time to when
    it is displayed via the API, allowing the recorded time taken to answer the card to be more accurate when calling
    `guiAnswerCard`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiStartCardTimer",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiShowQuestion`

*   Shows question text for the current card; returns `true` if in review mode or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiShowQuestion",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiShowAnswer`

*   Shows answer text for the current card; returns `true` if in review mode or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiShowAnswer",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiAnswerCard`

*   Answers the current card; returns `true` if succeeded or `false` otherwise. Note that the answer for the current
    card must be displayed before before any answer can be accepted by Anki.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiAnswerCard",
        "version": 6,
        "params": {
            "ease": 1
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiUndo`

*   Undo the last action / card; returns `true` if succeeded or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiUndo",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiDeckOverview`

*   Opens the *Deck Overview* dialog for the deck with the given name; returns `true` if succeeded or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiDeckOverview",
        "version": 6,
        "params": {
            "name": "Default"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiDeckBrowser`

*   Opens the *Deck Browser* dialog.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiDeckBrowser",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `guiDeckReview`

*   Starts review for the deck with the given name; returns `true` if succeeded or `false` otherwise.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiDeckReview",
        "version": 6,
        "params": {
            "name": "Default"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `guiImportFile`

*   Invokes the *Import... (Ctrl+Shift+I)* dialog with an optional file path. Brings up the dialog for user to review the import. Supports all file types that Anki supports. Brings open file dialog if no path is provided. Forward slashes must be used in the path on Windows. Only supported for Anki 2.1.52+.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiImportFile",
        "version": 6,
        "params": {
            "path": "C:/Users/Desktop/cards.txt"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `guiExitAnki`

*   Schedules a request to gracefully close Anki. This operation is asynchronous, so it will return immediately and
    won't wait until the Anki process actually terminates.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiExitAnki",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `guiCheckDatabase`

*   Requests a database check, but returns immediately without waiting for the check to complete. Therefore, the action will always return `true` even if errors are detected during the database check.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "guiCheckDatabase",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

---

### Media Actions

#### `storeMediaFile`

*   Stores a file with the specified base64-encoded contents inside the media folder. Alternatively you can specify a
    absolute file path, or a url from where the file shell be downloaded. If more than one of `data`, `path` and `url` are provided, the `data` field will be used first, then `path`, and finally `url`. To prevent Anki from removing files not used by any cards (e.g. for configuration files), prefix the filename with an underscore. These files are still synchronized to AnkiWeb.
    Any existing file with the same name is deleted by default. Set `deleteExisting` to false to prevent that
    by [letting Anki give the new file a non-conflicting name](https://github.com/ankitects/anki/blob/aeba725d3ea9628c73300648f748140db3fdd5ed/rslib/src/media/files.rs#L194).

    <details>
    <summary><i>Sample request (relative path):</i></summary>

    ```json
    {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": "_hello.txt",
            "data": "SGVsbG8sIHdvcmxkIQ=="
        }
    }
    ```

    *Content of `_hello.txt`*:

    ```
    Hello world!
    ```
    </details>

    <details>
    <summary><i>Sample result (relative path):</i></summary>

    ```json
    {
        "result": "_hello.txt",
        "error": null
    }
    ```
    </details>

    <details>
    <summary><i>Sample request (absolute path):</i></summary>

    ```json
    {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": "_hello.txt",
            "path": "/path/to/file"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result (absolute path):</i></summary>

    ```json
    {
        "result": "_hello.txt",
        "error": null
    }
    ```
    </details>

    <details>
    <summary><i>Sample request (url):</i></summary>

    ```json
    {
        "action": "storeMediaFile",
        "version": 6,
        "params": {
            "filename": "_hello.txt",
            "url": "https://url.to.file"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result (url):</i></summary>

    ```json
    {
        "result": "_hello.txt",
        "error": null
    }
    ```
    </details>

#### `retrieveMediaFile`

*   Retrieves the base64-encoded contents of the specified file, returning `false` if the file does not exist.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "retrieveMediaFile",
        "version": 6,
        "params": {
            "filename": "_hello.txt"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": "SGVsbG8sIHdvcmxkIQ==",
        "error": null
    }
    ```
    </details>

#### `getMediaFilesNames`

*   Gets the names of media files matched the pattern. Returning all names by default.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getMediaFilesNames",
        "version": 6,
        "params": {
            "pattern": "_hell*.txt"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["_hello.txt"],
        "error": null
    }
    ```
    </details>

#### `getMediaDirPath`

*   Gets the full path to the `collection.media` folder of the currently opened profile.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getMediaDirPath",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": "/home/user/.local/share/Anki2/Main/collection.media",
        "error": null
    }
    ```
    </details>

#### `deleteMediaFile`

*   Deletes the specified file inside the media folder.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "deleteMediaFile",
        "version": 6,
        "params": {
            "filename": "_hello.txt"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

---

### Miscellaneous Actions

#### `requestPermission`

*   Requests permission to use the API exposed by this plugin. This method does not require the API key, and is the
    only one that accepts requests from any origin; the other methods only accept requests from trusted origins,
    which are listed under `webCorsOriginList` in the add-on config. `localhost` is trusted by default.

    Calling this method from an untrusted origin will display a popup in Anki asking the user whether they want to
    allow your origin to use the API; calls from trusted origins will return the result without displaying the popup.
    When denying permission, the user may also choose to ignore further permission requests from that origin. These
    origins end up in the `ignoreOriginList`, editable via the add-on config.

    The result always contains the `permission` field, which in turn contains either the string `granted` or `denied`,
    corresponding to whether your origin is trusted. If your origin is trusted, the fields `requireApiKey` (`true` if
    required) and `version` will also be returned.

    This should be the first call you make to make sure that your application and Anki-Connect are able to communicate
    properly with each other. New versions of Anki-Connect are backwards compatible; as long as you are using actions
    which are available in the reported Anki-Connect version or earlier, everything should work fine.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "requestPermission",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample results:</i></summary>

    ```json
    {
        "result": {
            "permission": "granted",
            "requireApiKey": false,
            "version": 6
        },
        "error": null
    }
    ```

    ```json
    {
        "result": {
            "permission": "denied"
        },
        "error": null
    }
    ```
    </details>

#### `version`

*   Gets the version of the API exposed by this plugin. Currently versions `1` through `6` are defined.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "version",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 6,
        "error": null
    }
    ```
    </details>


#### `apiReflect`

*   Gets information about the AnkiConnect APIs available. The request supports the following params:

    * `scopes` - An array of scopes to get reflection information about.
      The only currently supported value is `"actions"`.
    * `actions` - Either `null` or an array of API method names to check for.
      If the value is `null`, the result will list all of the available API actions.
      If the value is an array of strings, the result will only contain actions which were in this array.

    The result will contain a list of which scopes were used and a value for each scope.
    For example, the `"actions"` scope will contain a `"actions"` property which contains a list of supported action names.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "apiReflect",
        "version": 6,
        "params": {
            "scopes": ["actions", "invalidType"],
            "actions": ["apiReflect", "invalidMethod"]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "scopes": ["actions"],
            "actions": ["apiReflect"]
        },
        "error": null
    }
    ```
    </details>

#### `sync`

*   Synchronizes the local Anki collections with AnkiWeb.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "sync",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `getProfiles`

*   Retrieve the list of profiles.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getProfiles",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["User 1"],
        "error": null
    }
    ```
    </details>

#### `loadProfile`

*   Selects the profile specified in request.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "loadProfile",
        "version": 6,
        "params": {
            "name": "user1"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `multi`

*   Performs multiple actions in one request, returning an array with the response of each action (in the given order).

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "multi",
        "version": 6,
        "params": {
            "actions": [
                {
                    "action": "deckNames"
                },
                {
                    "action": "deckNames",
                    "version": 6
                },
                {
                    "action": "invalidAction",
                    "params": {"useless": "param"}
                },
                {
                    "action": "invalidAction",
                    "params": {"useless": "param"},
                    "version": 6
                }
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
            ["Default"],
            {"result": ["Default"], "error": null},
            {"result": null, "error": "unsupported action"},
            {"result": null, "error": "unsupported action"}
        ],
        "error": null
    }
    ```
    </details>

#### `exportPackage`

*   Exports a given deck in `.apkg` format. Returns `true` if successful or `false` otherwise. The optional property
    `includeSched` (default is `false`) can be specified to include the cards' scheduling data.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "exportPackage",
        "version": 6,
        "params": {
            "deck": "Default",
            "path": "/data/Deck.apkg",
            "includeSched": true
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `importPackage`

*   Imports a file in `.apkg` format into the collection. Returns `true` if successful or `false` otherwise.
    Note that the file path is relative to Anki's collection.media folder, not to the client.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "importPackage",
        "version": 6,
        "params": {
            "path": "/data/Deck.apkg"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

#### `reloadCollection`

*   Tells anki to reload all data from the database.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "reloadCollection",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

---

### Model Actions

#### `modelNames`

*   Gets the complete list of model names for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelNames",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["Basic", "Basic (and reversed card)"],
        "error": null
    }
    ```
    </details>

#### `modelNamesAndIds`

*   Gets the complete list of model names and their corresponding IDs for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelNamesAndIds",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

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
    </details>

#### `findModelsById`

*   Gets a list of models  for the provided model IDs from the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "findModelsById",
        "version": 6,
        "params": {
            "modelIds": [1704387367119, 1704387398570]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
          {
            "id": 1704387367119,
            "name": "Basic",
            "type": 0,
            "mod": 1704387367,
            "usn": -1,
            "sortf": 0,
            "did": null,
            "tmpls": [
              {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": 9176047152973362695
              }
            ],
            "flds": [
              {
                "name": "Front",
                "ord": 0,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": 2453723143453745216,
                "tag": null,
                "preventDeletion": false
              },
              {
                "name": "Back",
                "ord": 1,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": -4853200230425436781,
                "tag": null,
                "preventDeletion": false
              }
            ],
            "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: center;\n    color: black;\n    background-color: white;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": false,
            "req": [
              [
                0,
                "any",
                [
                  0
                ]
              ]
            ],
            "originalStockKind": 1
          },
          {
            "id": 1704387398570,
            "name": "Basic (and reversed card)",
            "type": 0,
            "mod": 1704387398,
            "usn": -1,
            "sortf": 0,
            "did": null,
            "tmpls": [
              {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": 1689886528158874152
              },
              {
                "name": "Card 2",
                "ord": 1,
                "qfmt": "{{Back}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": -7839609225644824587
              }
            ],
            "flds": [
              {
                "name": "Front",
                "ord": 0,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": -7787837672455357996,
                "tag": null,
                "preventDeletion": false
              },
              {
                "name": "Back",
                "ord": 1,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": 6364828289839985081,
                "tag": null,
                "preventDeletion": false
              }
            ],
            "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: center;\n    color: black;\n    background-color: white;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": false,
            "req": [
              [
                0,
                "any",
                [
                  0
                ]
              ],
              [
                1,
                "any",
                [
                  1
                ]
              ]
            ],
            "originalStockKind": 1
          }
        ],
        "error": null
    }
    ```
    </details>


#### `findModelsByName`

*   Gets a list of models for the provided model names from the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "findModelsByName",
        "version": 6,
        "params": {
            "modelNames": ["Basic", "Basic (and reversed card)"]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
          {
            "id": 1704387367119,
            "name": "Basic",
            "type": 0,
            "mod": 1704387367,
            "usn": -1,
            "sortf": 0,
            "did": null,
            "tmpls": [
              {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": 9176047152973362695
              }
            ],
            "flds": [
              {
                "name": "Front",
                "ord": 0,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": 2453723143453745216,
                "tag": null,
                "preventDeletion": false
              },
              {
                "name": "Back",
                "ord": 1,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": -4853200230425436781,
                "tag": null,
                "preventDeletion": false
              }
            ],
            "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: center;\n    color: black;\n    background-color: white;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": false,
            "req": [
              [
                0,
                "any",
                [
                  0
                ]
              ]
            ],
            "originalStockKind": 1
          },
          {
            "id": 1704387398570,
            "name": "Basic (and reversed card)",
            "type": 0,
            "mod": 1704387398,
            "usn": -1,
            "sortf": 0,
            "did": null,
            "tmpls": [
              {
                "name": "Card 1",
                "ord": 0,
                "qfmt": "{{Front}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": 1689886528158874152
              },
              {
                "name": "Card 2",
                "ord": 1,
                "qfmt": "{{Back}}",
                "afmt": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}",
                "bqfmt": "",
                "bafmt": "",
                "did": null,
                "bfont": "",
                "bsize": 0,
                "id": -7839609225644824587
              }
            ],
            "flds": [
              {
                "name": "Front",
                "ord": 0,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": -7787837672455357996,
                "tag": null,
                "preventDeletion": false
              },
              {
                "name": "Back",
                "ord": 1,
                "sticky": false,
                "rtl": false,
                "font": "Arial",
                "size": 20,
                "description": "",
                "plainText": false,
                "collapsed": false,
                "excludeFromSearch": false,
                "id": 6364828289839985081,
                "tag": null,
                "preventDeletion": false
              }
            ],
            "css": ".card {\n    font-family: arial;\n    font-size: 20px;\n    text-align: center;\n    color: black;\n    background-color: white;\n}\n",
            "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost": "\\end{document}",
            "latexsvg": false,
            "req": [
              [
                0,
                "any",
                [
                  0
                ]
              ],
              [
                1,
                "any",
                [
                  1
                ]
              ]
            ],
            "originalStockKind": 1
          }
        ],
        "error": null
    }
    ```
    </details>

#### `modelFieldNames`

*   Gets the complete list of field names for the provided model name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldNames",
        "version": 6,
        "params": {
            "modelName": "Basic"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["Front", "Back"],
        "error": null
    }
    ```
    </details>

#### `modelFieldDescriptions`

*   Gets the complete list of field descriptions (the text seen in the gui editor when a field is empty) for the provided model name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldDescriptions",
        "version": 6,
        "params": {
            "modelName": "Basic"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["", ""],
        "error": null
    }
    ```
    </details>

#### `modelFieldFonts`

*   Gets the complete list of fonts along with their font sizes.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldFonts",
        "version": 6,
        "params": {
            "modelName": "Basic"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "Front": {
                "font": "Arial",
                "size": 20
            },
            "Back": {
                "font": "Arial",
                "size": 20
            }
        },
        "error": null
    }
    ```
    </details>

#### `modelFieldsOnTemplates`

*   Returns an object indicating the fields on the question and answer side of each card template for the given model
    name. The question side is given first in each array.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldsOnTemplates",
        "version": 6,
        "params": {
            "modelName": "Basic (and reversed card)"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "Card 1": [["Front"], ["Back"]],
            "Card 2": [["Back"], ["Front"]]
        },
        "error": null
    }
    ```
    </details>

#### `createModel`

*   Creates a new model to be used in Anki. User must provide the `modelName`, `inOrderFields` and `cardTemplates` to be
    used in the model. There are optional fields `css` and `isCloze`. If not specified, `css` will use the default Anki css and `isCloze` will be equal to `false`. If `isCloze` is `true` then model will be created as Cloze.

    Optionally the `Name` field can be provided for each entry of `cardTemplates`. By default the
    card names will be `Card 1`, `Card 2`, and so on.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "createModel",
        "version": 6,
        "params": {
            "modelName": "newModelName",
            "inOrderFields": ["Field1", "Field2", "Field3"],
            "css": "Optional CSS with default to builtin css",
            "isCloze": false,
            "cardTemplates": [
                {
                    "Name": "My Card 1",
                    "Front": "Front html {{Field1}}",
                    "Back": "Back html  {{Field2}}"
                }
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result":{
            "sortf":0,
            "did":1,
            "latexPre":"\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
            "latexPost":"\\end{document}",
            "mod":1551462107,
            "usn":-1,
            "vers":[

            ],
            "type":0,
            "css":".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n",
            "name":"TestApiModel",
            "flds":[
                {
                    "name":"Field1",
                    "ord":0,
                    "sticky":false,
                    "rtl":false,
                    "font":"Arial",
                    "size":20,
                    "media":[

                    ]
                },
                {
                    "name":"Field2",
                    "ord":1,
                    "sticky":false,
                    "rtl":false,
                    "font":"Arial",
                    "size":20,
                    "media":[

                    ]
                }
            ],
            "tmpls":[
                {
                    "name":"My Card 1",
                    "ord":0,
                    "qfmt":"",
                    "afmt":"This is the back of the card {{Field2}}",
                    "did":null,
                    "bqfmt":"",
                    "bafmt":""
                }
            ],
            "tags":[

            ],
            "id":1551462107104,
            "req":[
                [
                    0,
                    "none",
                    [

                    ]
                ]
            ]
        },
        "error":null
    }
    ```
    </details>

#### `modelTemplates`

*   Returns an object indicating the template content for each card connected to the provided model by name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelTemplates",
        "version": 6,
        "params": {
            "modelName": "Basic (and reversed card)"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "Card 1": {
                "Front": "{{Front}}",
                "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Back}}"
            },
            "Card 2": {
                "Front": "{{Back}}",
                "Back": "{{FrontSide}}\n\n<hr id=answer>\n\n{{Front}}"
            }
        },
        "error": null
    }
    ```
    </details>

#### `modelStyling`

*   Gets the CSS styling for the provided model by name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelStyling",
        "version": 6,
        "params": {
            "modelName": "Basic (and reversed card)"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "css": ".card {\n font-family: arial;\n font-size: 20px;\n text-align: center;\n color: black;\n background-color: white;\n}\n"
        },
        "error": null
    }
    ```
    </details>

#### `updateModelTemplates`

*   Modify the templates of an existing model by name. Only specifies cards and specified sides will be modified.
    If an existing card or side is not included in the request, it will be left unchanged.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateModelTemplates",
        "version": 6,
        "params": {
            "model": {
                "name": "Custom",
                "templates": {
                    "Card 1": {
                        "Front": "{{Question}}?",
                        "Back": "{{Answer}}!"
                    }
                }
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `updateModelStyling`

*   Modify the CSS styling of an existing model by name.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateModelStyling",
        "version": 6,
        "params": {
            "model": {
                "name": "Custom",
                "css": "p { color: blue; }"
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `findAndReplaceInModels`

*   Find and replace string in existing model by model name. Customise to replace in front, back or css by setting to true/false.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "findAndReplaceInModels",
        "version": 6,
        "params": {
            "model": {
                "modelName": "",
                "findText": "text_to_replace",
                "replaceText": "replace_with_text",
                "front": true,
                "back": true,
                "css": true
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1,
        "error": null
    }
    ```
    </details>

#### `modelTemplateRename`

*   Renames a template in an existing model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelTemplateRename",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "oldTemplateName": "Card 1",
            "newTemplateName": "Card 1 renamed"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelTemplateReposition`

*   Repositions a template in an existing model.

    The value of `index` starts at 0. For example, an index of `0` puts the template in the first position, and an index of `2` puts the template in the third position.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelTemplateReposition",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "templateName": "Card 1",
            "index": 1
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelTemplateAdd`

*   Adds a template to an existing model by name. If you want to update an existing template, use `updateModelTemplates`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelTemplateAdd",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "template": {
                "Name": "Card 3",
                "Front": "Front html {{Field1}}",
                "Back": "Back html {{Field2}}"
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelTemplateRemove`

*   Removes a template from an existing model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelTemplateRemove",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "templateName": "Card 1"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldRename`

*   Rename the field name of a given model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldRename",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "oldFieldName": "Front",
            "newFieldName": "FrontRenamed"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldReposition`

*   Reposition the field within the field list of a given model.

    The value of `index` starts at 0. For example, an index of `0` puts the field in the first position, and an index of `2` puts the field in the third position.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldReposition",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "Back",
            "index": 0
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldAdd`

*   Creates a new field within a given model.

    Optionally, the `index` value can be provided, which works exactly the same as the index in `modelFieldReposition`. By default, the field is added to the end of the field list.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldAdd",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "NewField",
            "index": 0
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldRemove`

*   Deletes a field within a given model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldRemove",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "Front"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldSetFont`

*   Sets the font for a field within a given model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldSetFont",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "Front",
            "font": "Courier"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldSetFontSize`

*   Sets the font size for a field within a given model.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldSetFontSize",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "Front",
            "fontSize": 10
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `modelFieldSetDescription`

*   Sets the description (the text seen in the gui editor when a field is empty) for a field within a given model.

    Older versions of Anki (2.1.49 and below) do not have field descriptions. In that case, this will return with `false`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "modelFieldSetDescription",
        "version": 6,
        "params": {
            "modelName": "Basic",
            "fieldName": "Front",
            "description": "example field description"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": true,
        "error": null
    }
    ```
    </details>

---

### Note Actions

#### `addNote`

*   Creates a note using the given deck and model, with the provided field values and tags. Returns the identifier of
    the created note created on success, and `null` on failure.

    Anki-Connect can download audio, video, and picture files and embed them in newly created notes. The corresponding `audio`, `video`, and `picture` note members are
    optional and can be omitted. If you choose to include any of them, they should contain a single object or an array of objects
    with the mandatory `filename` field and one of `data`, `path` or `url`. Refer to the documentation of `storeMediaFile` for an explanation of these fields.
    The `skipHash` field can be optionally provided to skip the inclusion of files with an MD5 hash that matches the provided value.
    This is useful for avoiding the saving of error pages and stub files.
    The `fields` member is a list of fields that should play audio or video, or show a picture when the card is displayed in
    Anki. The `allowDuplicate` member inside `options` group can be set to true to enable adding duplicate cards.
    Normally duplicate cards can not be added and trigger exception.

    The `duplicateScope` member inside `options` can be used to specify the scope for which duplicates are checked.
    A value of `"deck"` will only check for duplicates in the target deck; any other value will check the entire collection.

    The `duplicateScopeOptions` object can be used to specify some additional settings:

    * `duplicateScopeOptions.deckName` will specify which deck to use for checking duplicates in. If undefined or `null`, the target deck will be used.
    * `duplicateScopeOptions.checkChildren` will change whether or not duplicate cards are checked in child decks. The default value is `false`.
    * `duplicateScopeOptions.checkAllModels` specifies whether duplicate checks are performed across all note types. The default value is `false`.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "addNote",
        "version": 6,
        "params": {
            "note": {
                "deckName": "Default",
                "modelName": "Basic",
                "fields": {
                    "Front": "front content",
                    "Back": "back content"
                },
                "options": {
                    "allowDuplicate": false,
                    "duplicateScope": "deck",
                    "duplicateScopeOptions": {
                        "deckName": "Default",
                        "checkChildren": false,
                        "checkAllModels": false
                    }
                },
                "tags": [
                    "yomichan"
                ],
                "audio": [{
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": [
                        "Front"
                    ]
                }],
                "video": [{
                    "url": "https://cdn.videvo.net/videvo_files/video/free/2015-06/small_watermarked/Contador_Glam_preview.mp4",
                    "filename": "countdown.mp4",
                    "skipHash": "4117e8aab0d37534d9c8eac362388bbe",
                    "fields": [
                        "Back"
                    ]
                }],
                "picture": [{
                    "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/A_black_cat_named_Tilly.jpg/220px-A_black_cat_named_Tilly.jpg",
                    "filename": "black_cat.jpg",
                    "skipHash": "8d6e4646dfae812bf39651b59d7429ce",
                    "fields": [
                        "Back"
                    ]
                }]
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1496198395707,
        "error": null
    }
    ```
    </details>

#### `addNotes`

*   Creates multiple notes using the given deck and model, with the provided field values and tags. Returns an array of
    identifiers of the created notes. In the event of any errors, all errors are gathered and returned.
* Please see the documentation for `addNote` for an explanation of objects in the `notes` array.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
       "action":"addNotes",
       "version":6,
       "params":{
          "notes":[
             {
                "deckName":"College::PluginDev",
                "modelName":"non_existent_model",
                "fields":{
                   "Front":"front",
                   "Back":"bak"
                }
             },
             {
                "deckName":"College::PluginDev",
                "modelName":"Basic",
                "fields":{
                   "Front":"front",
                   "Back":"bak"
                }
             }
          ]
       }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
       "result":null,
       "error":"['model was not found: non_existent_model']"
    }
    ```
    </details>

#### `canAddNotes`

*   Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of
    booleans indicating whether or not the parameters at the corresponding index could be used to create a new note.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "canAddNotes",
        "version": 6,
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
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [true],
        "error": null
    }
    ```
    </details>

#### `canAddNotesWithErrorDetail`

*   Accepts an array of objects which define parameters for candidate notes (see `addNote`) and returns an array of
    objects with fields `canAdd` and `error`.

    * `canAdd` indicates whether or not the parameters at the corresponding index could be used to create a new note.
    * `error` contains an explanation of why a note cannot be added.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "canAddNotesWithErrorDetail",
        "version": 6,
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
                },
                {
                    "deckName": "Default",
                    "modelName": "Basic",
                    "fields": {
                        "Front": "front content 2",
                        "Back": "back content 2"
                    },
                    "tags": [
                        "yomichan"
                    ]
                }
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
            {
                "canAdd": false,
                "error": "cannot create note because it is a duplicate"
            },
            {
                "canAdd": true
            }
        ],
        "error": null
    }
    ```
    </details>

#### `updateNoteFields`

*   Modify the fields of an existing note. You can also include audio, video, or picture files which will be added to the note with an
    optional `audio`, `video`, or `picture` property. Please see the documentation for `addNote` for an explanation of objects in the `audio`, `video`, or `picture` array.

    > **Warning**:
    > You must not be viewing the note that you are updating on your Anki browser, otherwise
    > the fields will not update. See [this issue](https://github.com/FooSoft/anki-connect/issues/82)
    > for further details.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateNoteFields",
        "version": 6,
        "params": {
            "note": {
                "id": 1514547547030,
                "fields": {
                    "Front": "new front content",
                    "Back": "new back content"
                },
                "audio": [{
                    "url": "https://assets.languagepod101.com/dictionary/japanese/audiomp3.php?kanji=猫&kana=ねこ",
                    "filename": "yomichan_ねこ_猫.mp3",
                    "skipHash": "7e2c2f954ef6051373ba916f000168dc",
                    "fields": [
                        "Front"
                    ]
                }]
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `updateNote`

*   Modify the fields and/or tags of an existing note.
    In other words, combines `updateNoteFields` and `updateNoteTags`.
    Please see their documentation for an explanation of all properties.

    Either `fields` or `tags` property can be omitted without affecting the other.
    Thus valid requests to `updateNoteFields` also work with `updateNote`.
    The note must have the `fields` property in order to update the optional audio, video, or picture objects.

    If neither `fields` nor `tags` are provided, the method will fail.
    Fields are updated first and are not rolled back if updating tags fails.
    Tags are not updated if updating fields fails.

    > **Warning**
    > You must not be viewing the note that you are updating on your Anki browser, otherwise
    > the fields will not update. See [this issue](https://github.com/FooSoft/anki-connect/issues/82)
    > for further details.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateNote",
        "version": 6,
        "params": {
            "note": {
                "id": 1514547547030,
                "fields": {
                    "Front": "new front content",
                    "Back": "new back content"
                },
                "tags": ["new", "tags"]
            }
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `updateNoteModel`

* Update the model, fields, and tags of an existing note.
    This allows you to change the note's model, update its fields with new content, and set new tags.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateNoteModel",
        "version": 6,
        "params": {
            "note": {
                "id": 1514547547030,
                "modelName": "NewModel",
                "fields": {
                    "NewField1": "new field 1",
                    "NewField2": "new field 2",
                    "NewField3": "new field 3"
                },
                "tags": ["new", "updated", "tags"]
            }
        }
    }
    ```

    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```

    </details>

#### `updateNoteTags`

*   Set a note's tags by note ID. Old tags will be removed.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "updateNoteTags",
        "version": 6,
        "params": {
            "note": 1483959289817,
            "tags": ["european-languages"]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `getNoteTags`

*   Get a note's tags by note ID.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getNoteTags",
        "version": 6,
        "params": {
            "note": 1483959289817
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["european-languages"],
        "error": null
    }
    ```
    </details>

#### `addTags`

*   Adds tags to notes by note ID.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "addTags",
        "version": 6,
        "params": {
            "notes": [1483959289817, 1483959291695],
            "tags": "european-languages"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `removeTags`

*   Remove tags from notes by note ID.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "removeTags",
        "version": 6,
        "params": {
            "notes": [1483959289817, 1483959291695],
            "tags": "european-languages"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `getTags`

*   Gets the complete list of tags for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getTags",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": ["european-languages", "idioms"],
        "error": null
    }
    ```
    </details>

#### `clearUnusedTags`

*   Clears all the unused tags in the notes for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "clearUnusedTags",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `replaceTags`

*   Replace tags in notes by note ID.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "replaceTags",
        "version": 6,
        "params": {
            "notes": [1483959289817, 1483959291695],
            "tag_to_replace": "european-languages",
            "replace_with_tag": "french-languages"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `replaceTagsInAllNotes`

*   Replace tags in all the notes for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "replaceTagsInAllNotes",
        "version": 6,
        "params": {
            "tag_to_replace": "european-languages",
            "replace_with_tag": "french-languages"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `findNotes`

*   Returns an array of note IDs for a given query. Query syntax is [documented here](https://docs.ankiweb.net/searching.html).

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "findNotes",
        "version": 6,
        "params": {
            "query": "deck:current"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [1483959289817, 1483959291695],
        "error": null
    }
    ```
    </details>

#### `notesInfo`

*   Returns a list of objects containing for each note ID the note fields, tags, note type and the cards belonging to
    the note.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": [1502298033753]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

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
    </details>


#### `deleteNotes`

*   Deletes notes with the given ids. If a note has several cards associated with it, all associated cards will be deleted.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "deleteNotes",
        "version": 6,
        "params": {
            "notes": [1502298033753]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

#### `removeEmptyNotes`

*   Removes all the empty notes for the current user.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "removeEmptyNotes",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

---

### Statistic Actions

#### `getNumCardsReviewedToday`

*   Gets the count of cards that have been reviewed in the current day (with day start time as configured by user in anki)

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getNumCardsReviewedToday",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 0,
        "error": null
    }
    ```
    </details>

#### `getNumCardsReviewedByDay`

*   Gets the number of cards reviewed as a list of pairs of `(dateString, number)`

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getNumCardsReviewedByDay",
        "version": 6
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result":  [
            ["2021-02-28", 124],
            ["2021-02-27", 261]
        ],
        "error": null
    }
    ```
    </details>

#### `getCollectionStatsHTML`

*   Gets the collection statistics report

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getCollectionStatsHTML",
        "version": 6,
        "params": {
            "wholeCollection": true
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": "<center> lots of HTML here </center>",
        "error": null
    }
    ```
    </details>

#### `cardReviews`

*   Requests all card reviews for a specified deck after a certain time.
    `startID` is the latest unix time not included in the result.
    Returns a list of 9-tuples `(reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType)`

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "cardReviews",
        "version": 6,
        "params": {
            "deck": "default",
            "startID": 1594194095740
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": [
            [1594194095746, 1485369733217, -1, 3,   4, -60, 2500, 6157, 0],
            [1594201393292, 1485369902086, -1, 1, -60, -60,    0, 4846, 0]
        ],
        "error": null
    }
    ```
    </details>

#### `getReviewsOfCards`

*   Requests all card reviews for each card ID.
    Returns a dictionary mapping each card ID to a list of dictionaries of the format:
    ```
    {
        "id": reviewTime,
        "usn": usn,
        "ease": buttonPressed,
        "ivl": newInterval,
        "lastIvl": previousInterval,
        "factor": newFactor,
        "time": reviewDuration,
        "type": reviewType,
    }
    ```
    The reason why these key values are used instead of the more descriptive counterparts
    is because these are the exact key values used in Anki's database.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getReviewsOfCards",
        "version": 6,
        "params": {
            "cards": [
                "1653613948202"
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": {
            "1653613948202": [
                {
                    "id": 1653772912146,
                    "usn": 1750,
                    "ease": 1,
                    "ivl": -20,
                    "lastIvl": -20,
                    "factor": 0,
                    "time": 38192,
                    "type": 0
                },
                {
                    "id": 1653772965429,
                    "usn": 1750,
                    "ease": 3,
                    "ivl": -45,
                    "lastIvl": -20,
                    "factor": 0,
                    "time": 15337,
                    "type": 0
                }
            ]
        },
        "error": null
    }
    ```
    </details>

#### `getLatestReviewID`

*   Returns the unix time of the latest review for the given deck. 0 if no review has ever been made for the deck.

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "getLatestReviewID",
        "version": 6,
        "params": {
            "deck": "default"
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": 1594194095746,
        "error": null
    }
    ```
    </details>

#### `insertReviews`

*   Inserts the given reviews into the database. Required format: list of 9-tuples `(reviewTime, cardID, usn, buttonPressed, newInterval, previousInterval, newFactor, reviewDuration, reviewType)`

    <details>
    <summary><i>Sample request:</i></summary>

    ```json
    {
        "action": "insertReviews",
        "version": 6,
        "params": {
            "reviews": [
                [1594194095746, 1485369733217, -1, 3,   4, -60, 2500, 6157, 0],
                [1594201393292, 1485369902086, -1, 1, -60, -60,    0, 4846, 0]
            ]
        }
    }
    ```
    </details>

    <details>
    <summary><i>Sample result:</i></summary>

    ```json
    {
        "result": null,
        "error": null
    }
    ```
    </details>

---

# This docstring above is simply the AnkiConnect README.md from jully 2024. It's here for convenience but do checkout [the official AnkiConnect documentation](https://git.foosoft.net/alex/anki-connect).
"""
