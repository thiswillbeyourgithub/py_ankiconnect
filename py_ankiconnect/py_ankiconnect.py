from pathlib import Path
from typing import Union, List, Dict
import json
from urllib.error import URLError
import asyncio
import aiohttp
from functools import wraps

from .help import docstring


class PyAnkiconnect:
    VERSION: str = "1.1.0"

    def __init__(
        self,
        default_host: str = "http://127.0.0.1",
        default_port: int = 8765,
        force_async_mode: bool = False,
        timeout: int = 10,
        ) -> None:
        """
        Initialize a PyAnkiconnect instance.

        Parameters:
        -----------
        default_host : str, optional
            The host address for AnkiConnect. Defaults to "http://127.0.0.1".
        default_port : int, optional
            The port number for AnkiConnect. Defaults to 8765.
        force_async_mode : bool, optional
            Flag to always use asynchronous mode. Defaults to False, meaning
            that we use sync or async depending on the caller.
        timeout : int
            Nb of second to wait for the result when __sync_call__ decides to call
            async on its own (because it detects we are called in an async environment)


        Attributes:
        -----------
        host : str
        port : int
        force_async_mode : bool
        timeout : int

        Returns:
        --------
        None
        """
        self.host: str = default_host
        self.port: int = default_port
        self.force_async_mode = force_async_mode
        self.timeout = timeout

    def __call__(
        self,
        action: str,
        **params,
        ) -> Union[List, str]:
        if self.force_async_mode:
            return self.__async_call__(action, **params)
        else:
            return self.__sync_call__(action, **params)

    def __sync_call__(
        self,
        action: str,
        **params,
        ) -> Union[List, str]:
        if not asyncio.iscoroutinefunction(asyncio.current_task):
            loop = None
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError:
                try:
                    return asyncio.run(self.__async_call__(action=action, **params))
                except RuntimeError:
                    pass
            try:
                return self.__async_call__(action=action, **params)
            except Exception:
                pass

            if loop is not None:
                future = asyncio.run_coroutine_threadsafe(
                        self.__async_call__(action=action, **params),
                        loop,
                    )
                try:
                    result = future.result(timeout=self.timeout)
                    return result
                except TimeoutError:
                    raise Exception("Failed all ways to call sync or async_")
        else:
            return self.__async_call__(action=action, **params)

    async def __async_call__(
        self,
        action: str,
        **params,
    ) -> Union[List, str]:
        """
        Ask something from a running anki instance.
        **To see all the supported actions, see this class's docstring instead.**
        Note that if you are in an async environment, PyAnkiconnect will try to use the async code itself.

        Params:
        -------
        - action: str, for example 'sync'
        - params: dict, any parameters supported by the action.
            * With addition of "port" and "host" which,
                if specified will overide (for this call only) the value
                given at instanciation time.

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
        result = akc(
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
            raise Exception(
                "async_mode can only be used when instantiating the class, "
                "not when calling with it."
            )
        address: str = f"{host}:{port}"

        requestJson: bytes = json.dumps(
            {
                'action': action,
                'params': params,
                'version': 6
            }
        ).encode('utf-8')

        try:
            response: Dict = await self._async_request(address, requestJson)
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

        return response['result']


    async def _async_request(self, address: str, requestJson: bytes) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(address, data=requestJson) as response:
                assert response.ok, f"Status of response is not True but {response.ok}"
                assert response.status == 200, f"Status code of response is not 200 but {response.ok}"
                text = await response.text()
        try:
            data = json.loads(text)
        except Exception as err:
            raise Exception(f"Failed to decode json output of response: '{err}'")
        return data

# update the docstrings
PyAnkiconnect.__sync_call__.__doc__ = PyAnkiconnect.__async_call__.__doc__
PyAnkiconnect.__call__.__doc__ = PyAnkiconnect.__async_call__.__doc__
