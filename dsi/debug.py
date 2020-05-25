from pprint import pformat
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import Terminal256Formatter

from dsi.helpers import (
    caller_info,
    dsi_echo,
    dsi_err,
    json_dumps,
)


MARK_SCOPES = {}


def _format_args(*args, formatter=pformat):
    caller = caller_info(3)
    assert len(caller.arguments) == len(args)

    args_dict = {}
    for i in range(0, len(args)):
        args_dict[caller.arguments[i]] = args[i]

    args_formatted = []
    for key, value in args_dict.items():
        args_formatted.append(f"{key}={formatter(value)}")

    return args_formatted


def dump(*args):
    dsi_echo(", ".join(_format_args(*args)))


def dump_error(*args):
    dsi_err(", ".join(_format_args(*args)))


def dump_json(*args):
    def json_formatter(obj):
        return highlight(json_dumps(obj), JsonLexer(), Terminal256Formatter())
    dsi_echo(", ".join(_format_args(*args, formatter=json_formatter)))


def mark(scope="default"):
    if scope not in MARK_SCOPES:
        MARK_SCOPES[scope] = 0

    # @TODO: better output
    dsi_echo(f"MARK[{scope}][{MARK_SCOPES[scope]}]")
    MARK_SCOPES[scope] += 1
