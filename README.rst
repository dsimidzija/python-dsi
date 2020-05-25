dsi-utils
=========

Personal collection of ever-shifting utils & helpers for python.

Usage
-----

Installation
~~~~~~~~~~~~

If you're not me:

.. code-block:: bash

    pip install git+https://github.com/dsimidzija/python-dsi-utils.git#egg=dsi-utils

If you're me:

.. code-block:: bash

    git clone git@github.com-dsimidzija:dsimidzija/python-dsi-utils.git
    cd python-dsi-utils
    python setup.py develop

Now you can use:

.. code-block:: python

    import dsi
    dsi.d(yourvar)
    dsi.j(yourjsonvar)
    dsi.m("scope")

.. code-block:: bash

     DSI  yourfile.py:52(func_name): yourvar='some variable'
     DSI  yourfile.py:53(func_name): yourjsonvar={
      "but": [
        "we want to",
        "pretty print it for readability"
      ],
      "this": "is actually a dict",
      "timestamp": "2020-05-24T20:15:51.891180"
    }

     DSI  yourfile.py:54(func_name): MARK[scope][0]

* ``d`` is just a generic var-dumping helper
* ``j`` is the same, but uses JSON formatter to dump dicts
* ``m`` is a counter which you can use to track code branching

All of these should behave the same if you run them during a pytest run, i.e. ``dsi-utils`` will
register itself as a pytest plugin and disable output capture for own messages.

Vim
~~~

Using `UltiSnips`_:

.. _UltiSnips: https://github.com/SirVer/ultisnips

.. code-block:: snippets

    snippet dsid "dsi dump"
    import dsi; dsi.d(${1:variables})
    endsnippet

    snippet dsij "dsi json dump"
    import dsi; dsi.j(${1:variables})
    endsnippet

    snippet dsim "dsi mark"
    import dsi; dsi.m("${1:scope}")
    endsnippet
