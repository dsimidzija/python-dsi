import enum
import inspect
import os
import re
import token
import tokenize
import typing
from collections import namedtuple
from sys import stderr, stdout
from types import SimpleNamespace

import click
import simplejson

from dsi.pytest import called_from_pytest, disable_capture

ARGS_REGEX = re.compile(r"^(?P<call_code>[^\(]*)\((?P<call_args>.*)\)$")


class FunctionArgType(enum.Enum):
    REGULAR = enum.auto()
    ARGS = enum.auto()


FunctionArg = namedtuple("FunctionArg", ["text", "type"])


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


def caller_info(depth: int = 3) -> SimpleNamespace:
    stack = inspect.stack()
    args_frame = stack[depth][0]
    call_frame = stack[depth + 1][0]

    calling_line = inspect.getframeinfo(args_frame).code_context[0].strip()
    line_args_only = ARGS_REGEX.search(calling_line).group("call_args")
    iterator = iter([line_args_only])
    tokens = tokenize.generate_tokens(lambda: next(iterator))
    calling_args = extract_args_from_tokens(tokens)

    return SimpleNamespace(
        function_name=call_frame.f_code.co_name,
        filename=os.path.basename(call_frame.f_code.co_filename),
        line_number=call_frame.f_lineno,
        arguments=calling_args,
    )


def extract_args_from_tokens(tokens: typing.List[tokenize.TokenInfo]) -> typing.List:
    """Use python tokenizer to figure out the proper params used to call us."""
    output = []
    name = ""
    type_ = FunctionArgType.REGULAR
    depth = 0

    for token_ in tokens:
        if depth > 0:
            name += token_.string
            if token_.exact_type in (token.RPAR, token.RBRACE, token.RSQB):
                depth -= 1
        elif depth == 0:
            if token_.type not in (token.OP, token.NEWLINE, token.ENDMARKER):
                name += token_.string
                continue
            if token_.type in (token.NEWLINE, token.ENDMARKER):
                output.append(FunctionArg(name, type_))
                break

            if token_.exact_type == token.COMMA:
                output.append(FunctionArg(name, type_))
                name = ""
                type_ = FunctionArgType.REGULAR
            elif token_.exact_type == token.STAR:
                if name == "":
                    type_ = FunctionArgType.ARGS
                name += token_.string
            elif token_.exact_type in (token.LPAR, token.LBRACE, token.LSQB):
                name += token_.string
                depth += 1
            else:
                name += token_.string

    return output


def json_dumps(obj: typing.Any) -> str:
    def default_impl(o):
        if hasattr(o, "isoformat"):
            return o.isoformat()
        raise TypeError()

    return simplejson.dumps(obj, indent=2, sort_keys=True, default=default_impl)
