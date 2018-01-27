===============================
Welcome to python-bigone v0.0.2
===============================

.. image:: https://img.shields.io/pypi/v/python-bigone.svg
    :target: https://pypi.python.org/pypi/python-bigone

.. image:: https://img.shields.io/pypi/l/python-bigone.svg
    :target: https://pypi.python.org/pypi/python-bigone

.. image:: https://img.shields.io/travis/sammchardy/python-bigone.svg
    :target: https://travis-ci.org/sammchardy/python-bigone

.. image:: https://img.shields.io/coveralls/sammchardy/python-bigone.svg
    :target: https://coveralls.io/github/sammchardy/python-bigone

.. image:: https://img.shields.io/pypi/wheel/python-bigone.svg
    :target: https://pypi.python.org/pypi/python-bigone

.. image:: https://img.shields.io/pypi/pyversions/python-bigone.svg
    :target: https://pypi.python.org/pypi/python-bigone

This is an unofficial Python wrapper for the `BigONE exchanges REST API v1 <https://developer.big.one/>`_. I am in no way affiliated with BigONE, use at your own risk.

PyPi
  https://pypi.python.org/pypi/python-bigone

Source code
  https://github.com/sammchardy/python-bigone

Documentation
  https://python-bigone.readthedocs.io/en/latest/


Features
--------

- Implementation of all REST endpoints
- Simple handling of authentication
- Response exception handling

Quick Start
-----------

Register an account with `BigONE <https://big.one/>`_.

`Generate an API Key <https://big.one/settings>`_ and store it.

.. code:: bash

    pip install python-bigone


.. code:: python

    from bigone.client import Client
    client = Client(api_key)

    # get markets
    markets = client.get_markets()

    # get market order book
    depth = client.get_order_book('ETH-BTC')

    # get market trades
    trades = client.get_market_trades('ETH-BTC')

    # get your accounts
    currencies = client.get_accounts()

    # place a bid order
    transaction = client.create_order('KCS-BTC', Client.SIDE_BID, '0.01', '1000')

    # place an ask order
    transaction = client.create_order('KCS-BTC', Client.SIDE_ASK, '0.01', '1000')

    # get a list of your orders for a symbol
    orders = client.get_orders('ETH-BTC')

    # get a list of your trades for a symbol
    orders = client.get_trades('ETH-BTC')

    # withdraw a currency
    res = client.withdraw(
                '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX',
                'BTC',
                '0.590464',
                '0.002',
                'your currency pin',
                'some label notes')

    # get list of all withdrawals
    withdrawals = client.get_withdrawals()

    # get list of withdrawals for BTC
    withdrawals = client.get_withdrawals('BTC')

    # get list of all deposits
    deposits = client.get_deposits()

    # get list of deposits for BTC
    deposits = client.get_deposits('BTC')


For more `check out the documentation <https://python-bigone.readthedocs.io/en/latest/>`_.

Donate
------

If this library helped you out feel free to donate.

- ETH: 0xD7a7fDdCfA687073d7cC93E9E51829a727f9fE70
- NEO: AVJB4ZgN7VgSUtArCt94y7ZYT6d5NDfpBo
- LTC: LPC5vw9ajR1YndE1hYVeo3kJ9LdHjcRCUZ
- BTC: 1Dknp6L6oRZrHDECRedihPzx2sSfmvEBys

Other Exchanges
---------------

If you use `Binance <https://www.binance.com/?ref=10099792>`_ check out my `python-binance <https://github.com/sammchardy/python-binance>`_ library.

If you use `Kucoin <https://www.kucoin.com/#/?r=E42cWB>`_ check out my `python-kucoin <https://github.com/sammchardy/python-kucoin>`_ library.

If you use `Quoinex <https://accounts.quoinex.com/sign-up?affiliate=PAxghztC67615>`_
or `Qryptos <https://accounts.qryptos.com/sign-up?affiliate=PAxghztC67615>`_ check out my `python-quoine <https://github.com/sammchardy/python-quoine>`_ library.

If you use `IDEX <https://idex.market>`_ check out my `python-idex <https://github.com/sammchardy/python-idex>`_ library.

.. image:: https://analytics-pixel.appspot.com/UA-111417213-1/github/python-bigone?pixel