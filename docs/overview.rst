Getting Started
===============

Installation
------------

``python-bigone`` is available on `PYPI <https://pypi.python.org/pypi/python-bigone/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-bigone


Register on Big.One
-------------------

Firstly register an account with `Big.One <https://big.one>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key <https://big.one/settings>`_ and store it.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from bigone.client import Client
    client = Client(api_key)

API Rate Limit
--------------

No information
