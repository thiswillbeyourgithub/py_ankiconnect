import fire

from .py_ankiconnect import PyAnkiconnect


__all__ = ["PyAnkiconnect"]

__VERSION__ = PyAnkiconnect.VERSION

def cli_launcher() -> None:
    args, kwargs = fire.Fire(
        lambda *args, **kwargs: [args, kwargs]
    )
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
        akc.called_from_cli = True
        out = akc(*args, **kwargs)
        print(out)
        return

if __name__ == "__main__":
    cli_launcher()
