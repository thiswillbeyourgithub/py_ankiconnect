from pathlib import Path
from typing import Union, List, Dict
import json
import urllib.request
from urllib.error import URLError
import asyncio
import aiohttp

class PyAnkiconnect:
    VERSION: str = "0.1.2"
    called_from_cli: bool = False

    def __init__(
        self,
        default_host: str = "http://127.0.0.1",
        default_port: int = 8765,
        async_mode: bool = False,
        ) -> None:
        """
        Initialize a PyAnkiconnect instance.

        Parameters:
        -----------
        default_host : str, optional
            The host address for AnkiConnect. Defaults to "http://127.0.0.1".
        default_port : int, optional
            The port number for AnkiConnect. Defaults to 8765.
        async_mode : bool, optional
            Flag to enable asynchronous mode. Defaults to False.

        Attributes:
        -----------
        host : str
            The default host address for AnkiConnect.
        port : int
            The default port number for AnkiConnect.
        async_mode : bool
            Flag indicating if the instance should operate in asynchronous mode.
        called_from_cli : bool
            Flag indicating if the instance is being created from a CLI. Defaults to False.
            You should never have to modify it manually.

        Returns:
        --------
        None
        """
        self.host: str = default_host
        self.port: int = default_port
        self.async_mode: bool = async_mode

    async def __call__(
        self,
        action: str,
        **params,
    ) -> Union[List, str]:
        """
        Ask something from a running anki instance.
        **To see all the supported actions, see this class's docstring instead.**

        Params:
        -------
        - action: str, for example 'sync'
        - params: dict, any parameters supported by the action.
            * With addition of "port", "host" and "called_from_cli" which,
              if specified will overide (for this call only) the value
              given at instanciation time.

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
        import asyncio

        async def main():
            akc = PyAnkiconnect()
            # ^ You can set a different port or host there directly:
            # akc = PyAnkiconnect(port=your_port)

            # trigger a sync:
            result = await akc("sync")

            # Get the list of all tags:
            result = await akc("getTags")

            # Do some more advanced stuff:
            result = await akc(
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

        asyncio.run(main())
        ```

        **To see all the supported actions, see this class's docstring instead.**
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
        if "async_mode" in params:
            async_mode = params["async_mode"]
            del params["async_mode"]
        else:
            async_mode = self.async_mode
        address: str = f"{host}:{port}"

        requestJson: bytes = json.dumps(
            {
                'action': action,
                'params': params,
                'version': 6
            }
        ).encode('utf-8')

        try:
            if async_mode:
                response: Dict = await self._async_request(address, requestJson)
            else:
                response: Dict = self._sync_request(address, requestJson)
        except (ConnectionRefusedError, URLError, aiohttp.ClientError) as e:
            raise Exception(
                f"Error: '{str(e)}': is Anki open? is ankiconnect enabled? "
                f"is your firewall configured? Address is '{address}'"
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

        if self.called_from_cli:
            return json.dumps(response['result'])
        else:
            return response['result']


# set the docstring
docstring_file = Path(__file__).parent / "help.md"
docstring = docstring_file.read_text()
PyAnkiconnect.__doc__ = docstring
    async def _async_request(self, address: str, requestJson: bytes) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(address, data=requestJson) as response:
                return await response.json()

    def _sync_request(self, address: str, requestJson: bytes) -> Dict:
        return json.load(
            urllib.request.urlopen(
                urllib.request.Request(
                    address,
                    requestJson
                )
            )
        )
