from pathlib import Path
from typing import Union, List, Dict
import json
from urllib.error import URLError
import asyncio
import aiohttp
from functools import wraps


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
        if async_mode:
            self.__class__.__call__ = self.__class__.__async_call__
        else:
            self.__class__.__call__ = self.__class__.__sync_call__
        self.async_mode = async_mode

    def __sync_call__(self, *args, **kwargs) -> Union[List, str]:
        return asyncio.run(self.__async_call__(*args, **kwargs))

    async def __async_call__(
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

        if self.called_from_cli:
            return json.dumps(response['result'])
        else:
            return response['result']


    async def _async_request(self, address: str, requestJson: bytes) -> Dict:
        async with aiohttp.ClientSession() as session:
            async with session.post(address, data=requestJson) as response:
                return await response.json()


# make sure both calls have the same info
PyAnkiconnect.__sync_call__ = wraps(PyAnkiconnect.__async_call__)(PyAnkiconnect.__sync_call__)

# set the docstring
docstring_file = Path(__file__).parent / "help.md"
docstring = docstring_file.read_text()
PyAnkiconnect.__doc__ = docstring

if __name__ == "__main__":
    import time
    import asyncio

    n = 10

    # Single synchronous call
    akc_sync = PyAnkiconnect(async_mode=False)
    start_time_sync = time.time()
    ref = akc_sync("getTags")
    end_time_sync = time.time()
    sync_time = end_time_sync - start_time_sync
    print(f"Time for 1 synchronous request: {sync_time:.2f} seconds")

    async def async_sleep_timer():
        start = time.time()
        await asyncio.sleep(1)
        end = time.time()
        return end - start

    async def run_test(n):
        start_time = time.time()
        akc = PyAnkiconnect(async_mode=True)
        
        # Create tasks for getTags and sleep timer
        tag_tasks = [akc("getTags") for _ in range(n)]
        sleep_task = asyncio.create_task(async_sleep_timer())
        
        # Gather all tasks
        results = await asyncio.gather(*tag_tasks, sleep_task)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # The last result is from the sleep timer
        sleep_time = results[-1]
        tag_results = results[:-1]
        
        return tag_results, total_time, sleep_time

    tag_results, total_time, sleep_time = asyncio.run(run_test(n))

    print(f"Total time for {n} asynchronous requests: {total_time:.2f} seconds")
    print(f"Average time per asynchronous request: {total_time/n:.2f} seconds")
    print(f"Sleep timer duration: {sleep_time:.2f} seconds")

    if total_time < sync_time * n:
        print("The asynchronous requests were indeed faster!")
    else:
        print("The asynchronous requests might not be optimized. Check your implementation.")

    if sleep_time >= 1.0 and total_time > sleep_time:
        print("The sleep timer ran concurrently with the requests, demonstrating asynchronous behavior!")
    else:
        print("The sleep timer might not have run concurrently. Check the implementation.")

    assert all(r == ref for r in tag_results), "results are not identical"

