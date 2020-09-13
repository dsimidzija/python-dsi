from datetime import datetime

import click

from dsi.debug import dump, dump_error, dump_json


@click.group()
def main():
    pass


@main.command()
def self_test():
    """Perform minimal self-tests."""

    class TestyMcTesticles:
        def __init__(self, value):
            self.value = value

        def __repr__(self):
            return f'{__class__.__name__}("{self.value}")'

    debugvar1 = "one"
    debugvar2 = "two"
    debugvar3 = {
        "some dict": "stringval",
        "nao": datetime.utcnow(),
        "decimal": 3.14,
    }
    debugvar4 = TestyMcTesticles("drink!")
    debugvar5 = {
        "otherdict": {"nested": "dict"},
    }

    dump(debugvar1, debugvar2)
    dump(debugvar3, debugvar4)
    dump_error(debugvar3, debugvar4)
    dump_json(debugvar3, debugvar5)
