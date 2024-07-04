import fire

from .py_ankiconnect import PyAnkiconnect


__all__ = ["PyAnkiconnect"]

__VERSION__ = PyAnkiconnect.VERSION

def cli_launcher() -> None:
    args, kwargs = fire.Fire(
        lambda *args, **kwargs: [args, kwargs]
    )
    if "help" in args or ("help" in kwargs and kwargs["help"]):
        fire.Fire(PyAnkiconnect)
    else:
        fire.Fire(PyAnkiconnect().call)

if __name__ == "__main__":
    cli_launcher()
