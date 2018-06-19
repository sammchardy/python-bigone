Getting Started
===============

Installation
------------

``python-bigone`` is available on `PYPI <https://pypi.python.org/pypi/python-bigone/>`_.
Install with ``pip``:

.. code:: bash

    pip install python-bigone


Register on BigONE
------------------

Firstly register an account with `BigONE <https://big.one>`_.

Generate an API Key
-------------------

To use signed account methods you are required to `create an API Key <https://big.one/settings/api-keys>`_ and store it.

Initialise the client
---------------------

Pass your API Key and Secret

.. code:: python

    from bigone.client import Client
    client = Client(api_key, api_secret)

API Rate Limit
--------------

No information
