import fire

from .py_ankiconnect import PyAnkiconnect

__all__ = ["PyAnkiconnect"]

__VERSION__ = PyAnkiconnect.VERSION

def cli_launcher() -> None:
    fire.Fire(PyAnkiconnect)

if __name__ == "__main__":
    cli_launcher()