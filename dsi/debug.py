import typing
from pprint import pformat

from pygments import highlight
from pygments.formatters import Terminal256Formatter
from pygments.lexers import JsonLexer

from dsi.helpers import (
    FunctionArg,
    FunctionArgType,
    caller_info,
    dsi_echo,
    dsi_err,
    json_dumps,
)

MARK_SCOPES = {}


def _format_args(
    *args: typing.Any, formatter: typing.Callable = pformat
) -> typing.List:
    """Format caller args as `name=value`.

    The main tricky thing here is that we need to handle cases where caller args
    do not match the args we received, i.e. we have one or more `*args` in there.
    When there is one, we handle it by counting the args, but when there are multiple,
    we have no way of knowing which value belongs to which arg, so just print
    everything with a question mark in place of the argument name.
    """
    caller = caller_info(3)
    args_formatted = []
    posargs_count = sum(1 for i in caller.arguments if i.type == FunctionArgType.ARGS)

    if len(caller.arguments) == len(args):
        for key, value in zip(caller.arguments, args):
            args_formatted.append(f"{key.text}={formatter(value)}")
    elif len(caller.arguments) == 1:
        value_str = ", ".join(formatter(value) for value in args)
        args_formatted.append(f"{caller.arguments[0].text}=({value_str})")
    elif posargs_count == 1:
        arg_diff = len(args) - len(caller.arguments)
        assert arg_diff > 0

        values_index = 0
        for index, arg in enumerate(caller.arguments):
            if arg.type != FunctionArgType.ARGS:
                args_formatted.append(f"{arg.text}={formatter(args[values_index])}")
                values_index += 1
            else:
                value_str = ", ".join(
                    formatter(value)
                    for value in args[values_index : (values_index + arg_diff + 1)]
                )
                values_index += arg_diff + 1
                args_formatted.append(f"{arg.text}=({value_str})")
    else:  # multiple *args, just wing it
        dummy_args = [FunctionArg("?", FunctionArgType.REGULAR)] * len(args)
        for key, value in zip(dummy_args, args):
            args_formatted.append(f"{key.text}={formatter(value)}")

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
