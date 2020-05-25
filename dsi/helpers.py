from sys import (
    stdout,
    stderr,
)
from types import SimpleNamespace
import inspect
import os
import re

import click
import simplejson

from dsi.pytest import (
    called_from_pytest,
    disable_capture,
)


ARGS_REGEX = re.compile(r"\((.*?)\).*$")


def _secho(*args, **kwargs):
    if called_from_pytest():
        with disable_capture():
            click.secho(*args, **kwargs)
    else:
        click.secho(*args, **kwargs)


def echo(message, dsi_file=stdout, dsi_fg="black", dsi_bg="yellow", **kwargs):
    """Output to stdout/stderr, with extras.

    * Adds a coloured marker for visibility.
    * Adds caller info."""
    caller = caller_info()
    extras = f"{caller.filename}:{caller.line_number}({caller.function_name})"
    _secho(" DSI ", file=dsi_file, fg=dsi_fg, bg=dsi_bg, nl=False)
    _secho(f" {extras}: ", file=dsi_file, nl=False)
    _secho(message, dsi_file, **kwargs)


def dsi_err(message, **kwargs):
    echo(message, dsi_file=stderr, dsi_fg="black", dsi_bg="red", **kwargs)


def dsi_echo(message, **kwargs):
    echo(message, dsi_file=stderr, dsi_fg="black", dsi_bg="yellow", **kwargs)


def caller_info(depth=3):
    stack = inspect.stack()
    args_frame = stack[depth][0]
    call_frame = stack[depth+1][0]

    calling_line = inspect.getframeinfo(args_frame).code_context[0].strip()
    calling_args = ARGS_REGEX.search(calling_line).groups()[0].split(",")
    calling_args = list(map(lambda x: x.strip(), calling_args))

    return SimpleNamespace(
        function_name=call_frame.f_code.co_name,
        filename=os.path.basename(call_frame.f_code.co_filename),
        line_number=call_frame.f_lineno,
        arguments=calling_args,
    )


def json_dumps(obj):
    def default_impl(o):
        if hasattr(o, "isoformat"):
            return o.isoformat()
        raise TypeError()

    return simplejson.dumps(obj, indent=2, sort_keys=True, default=default_impl)
