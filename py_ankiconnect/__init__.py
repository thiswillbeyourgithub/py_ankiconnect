import json
import fire

from .py_ankiconnect import PyAnkiconnect


__all__ = ["PyAnkiconnect"]

__VERSION__ = PyAnkiconnect.VERSION

def cli_launcher() -> None:
    args, kwargs = fire.Fire(
        lambda *args, **kwargs: [args, kwargs]
    )

    # fire replaces notes to "tes" because it removes leading no
    for keyword in ["notes", "notetypes"]:
        if keyword[2:] in kwargs:
            kwargs[keyword] = kwargs[keyword[2:]]
            del kwargs[keyword[2:]]

    if "help" in args or ("help" in kwargs and kwargs["help"]):
        try:
            # if possible use rich because it's in markdown
            from rich.console import Console
            from rich.markdown import Markdown
            console = Console()
            md = Markdown(PyAnkiconnect.__doc__)
            console.print(md)
        except Exception:
            # print it
            print(PyAnkiconnect.__doc__)
            # open the pager
            fire.Fire(PyAnkiconnect)
    else:
        akc = PyAnkiconnect()
        out = akc(*args, **kwargs)
        try:
            out = json.dumps(out, ensure_ascii=False, pretty=False)
        except Exception:
            pass
        try:
            print(out)
        except Exception:
            return out

if __name__ == "__main__":
    cli_launcher()
