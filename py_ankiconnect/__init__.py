import json
import fire
import sys

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

    # if "-" is in sys.argv, parse the last line of stdin as a json output
    if "-" in sys.argv:
        target_key = sys.argv[sys.argv.index("-") - 1][2:]
        import signal
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        piped_lines = []
        try:
            for line in sys.stdin:
                piped_lines.append(line)
        except BrokenPipeError:
            # Handle the error gracefully
            sys.stderr.close()
        piped_lines = [p.strip() for p in piped_lines if p.strip()]

        if piped_lines:
            try:
                piped_values = json.loads(piped_lines[-1])
            except Exception:
                piped_values = piped_lines[-1]
            # if it's a list and contains only str that looks like int, cast as it (for example --notes)
            if isinstance(piped_values, list):
                if all(str(val).isdigit() for val in piped_values):
                    piped_values = [int(val) for val in piped_values]
            assert kwargs[target_key] is False
            kwargs[target_key] = piped_values

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
