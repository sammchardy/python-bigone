# coding=utf-8

import requests

from uuid import uuid4
from .exceptions import BigoneAPIException, BigoneRequestException


class Client(object):

    API_URL = 'https://api.big.one'

    SIDE_BID = 'BID'
    SIDE_ASK = 'ASK'

    def __init__(self, api_key):
        """Big.One API Client constructor

        https://developer.big.one/

        :param api_key: Api Token Id
        :type api_key: str

        .. code:: python

            client = Client(api_key)

        """

        self.API_KEY = api_key
        self.UUID = self._get_uuid()
        self.session = self._init_session()

    def _get_uuid(self):
        return str(uuid4())

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-bigone',
                   'Authorization': 'Bearer {}'.format(self.API_KEY),
                   'Big-Device-Id': self.UUID}
        session.headers.update(headers)
        return session

    def _create_uri(self, path):
        return '{}/{}'.format(self.API_URL, path)

    def _request(self, method, path, signed, **kwargs):

        data = kwargs.get('data', None)

        uri = self._create_uri(path)

        if method == 'get' and data:
            kwargs['params'] = kwargs['data']
            del(kwargs['data'])

        if method == 'post' and data:
            kwargs['json'] = kwargs['data']
            del(kwargs['data'])

        response = getattr(self.session, method)(uri, **kwargs)
        return self._handle_response(response)

    def _handle_response(self, response):
        """Internal helper for handling API responses from the Quoine server.
        Raises the appropriate exceptions when necessary; otherwise, returns the
        response.
        """

        if not str(response.status_code).startswith('2'):
            raise BigoneAPIException(response)
        try:
            json = response.json()

            if 'success' in json and not json['success']:
                raise BigoneAPIException(response)

            # by default return full response
            res = json
            # if it's a normal response we have a data attribute, return that
            if 'data' in json:
                res = json['data']
            return res
        except ValueError:
            raise BigoneRequestException('Invalid Response: %s' % response.text)

    def _get(self, path, signed=False, **kwargs):
        return self._request('get', path, signed, **kwargs)

    def _post(self, path, signed=False, **kwargs):
        return self._request('post', path, signed, **kwargs)

    def _put(self, path, signed=False, **kwargs):
        return self._request('put', path, signed, **kwargs)

    def _delete(self, path, signed=False, **kwargs):
        return self._request('delete', path, signed, **kwargs)

    # Account endpoints

    def get_accounts(self):
        """List accounts of current user

        .. code:: python

            accounts = client.get_accounts()

        :return: list of dicts

        .. code:: python

            [
                {
                    "type": "account",
                    "user_id": "5c1b7700-c903-41f8-9b4c-d78be9b2685d",
                    "account_id": "7eb4201b-9ae8-450d-819a-1c7dfd272e3d",
                    "account_type": "BTC",
                    "account_name": "Bitcoin",
                    "account_logo_url": "https://storage.googleapis.com/big-one/coins/BTC.svg",
                    "public_key": "16zy7YGERPEygQitMFaqP4afPJBZeo2WK6",
                    "system_account": "",
                    "active_balance": "0.00000000",
                    "frozen_balance": "0.00000000",
                    "estimated_btc_price": "1.00000000",
                    "verification": "EMAIL_VERIFIED",
                    "has_asset_pin": false
                },
                {
                    "type": "account",
                    "user_id": "5c1b7700-c903-41f8-9b4c-d78be9b2685d",
                    "account_id": "3d7c2353-add3-4e03-8637-c78e4d2b17cb",
                    "account_type": "ETH",
                    "account_name": "Ether",
                    "account_logo_url": "https://storage.googleapis.com/big-one/coins/ETH.svg",
                    "public_key": "0xaefde180aae6e0916632dabfdd2f8733c8a03826",
                    "system_account": "",
                    "active_balance": "0.00000000",
                    "frozen_balance": "0.00000000",
                    "estimated_btc_price": "0.06500000",
                    "verification": "EMAIL_VERIFIED",
                    "has_asset_pin": false
                }
            ]

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('accounts', True)

    def get_account(self, currency):
        """Get account for a currency

        :param currency: Name of currency
        :type currency: str

        .. code:: python

            account = client.get_account('BTC')

        :return: dict

        .. code:: python

            {
                "type": "account",
                "user_id": "5c1b7700-c903-41f8-9b4c-d78be9b2685d",
                "account_id": "7eb4201b-9ae8-450d-819a-1c7dfd272e3d",
                "account_type": "BTC",
                "account_name": "Bitcoin",
                "account_logo_url": "https://storage.googleapis.com/big-one/coins/BTC.svg",
                "public_key": "16zy7YGERPEygQitMFaqP4afPJBZeo2WK6",
                "system_account": "",
                "active_balance": "0.00000000",
                "frozen_balance": "0.00000000",
                "estimated_btc_price": "1.00000000",
                "verification": "EMAIL_VERIFIED",
                "has_asset_pin": false,
                "withdrawal": {
                "fee": "0.002",
                "fee_type": "BTC"
                },
                "deposits": [],
                "withdrawals": [],
                "recipients": []
            }

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('accounts/{}'.format(currency), True)

    # Market endpoints

    def get_markets(self):
        """List markets

        .. code:: python

            markets = client.get_markets()

        :return: list of dicts

        .. code:: python

            [
                {
                    "type": "market",
                    "symbol": "EKT-BTC",
                    "base": "BTC",
                    "quote": "EKT",
                    "base_min": "0.00000001",
                    "base_max": "1000000",
                    "quote_increment": "1",
                    "total_min": "0.001",
                    "base_name": "Bitcoin",
                    "quote_name": "EDUCare",
                    "ticker": {
                        "price": "0.00000830",
                        "low": "0.00000533",
                        "high": "0.00000997",
                        "open": "0.00000899",
                        "close": "0.00000830",
                        "volume": "678344.00000000"
                    },
                    "metrics": {
                        "0000060": [
                            [
                                1516150800000,
                                "0.00000641",
                                "0.00000641",
                                "0.00000641",
                                "0.00000641",
                                "6593.00000000"
                            ],
                            [
                                1516147200000,
                                "0.00000840",
                                "0.00000840",
                                "0.00000840",
                                "0.00000840",
                                "0.00000000"
                            ],
                            [
                                1516143600000,
                                "0.00000840",
                                "0.00000840",
                                "0.00000840",
                                "0.00000840",
                                "0.00000000"
                            ],
                        ]
                    },
                    "trades": [],
                    "asks": [],
                    "bids": [],
                    "depth": {
                        "type": "depth",
                        "asks": [],
                        "bids": []
                    },
                    "accounts": []
                }
            ]

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('markets', True)

    def get_market(self, symbol):
        """Get symbol market details

        :param symbol: Name of symbol
        :type symbol: str

        .. code:: python

            market = client.get_market('ETH-BTC')

        :return: dict

        .. code:: python

            {
                "type": "market",
                "symbol": "EKT-BTC",
                "base": "BTC",
                "quote": "EKT",
                "base_min": "0.00000001",
                "base_max": "1000000",
                "quote_increment": "1",
                "total_min": "0.001",
                "base_name": "Bitcoin",
                "quote_name": "EDUCare",
                "ticker": {
                    "price": "0.00000830",
                    "low": "0.00000533",
                    "high": "0.00000997",
                    "open": "0.00000899",
                    "close": "0.00000830",
                    "volume": "678344.00000000"
                },
                "metrics": {
                    "0000060": [
                        [
                            1516150800000,
                            "0.00000641",
                            "0.00000641",
                            "0.00000641",
                            "0.00000641",
                            "6593.00000000"
                        ],
                        [
                            1516147200000,
                            "0.00000840",
                            "0.00000840",
                            "0.00000840",
                            "0.00000840",
                            "0.00000000"
                        ],
                        [
                            1516143600000,
                            "0.00000840",
                            "0.00000840",
                            "0.00000840",
                            "0.00000840",
                            "0.00000000"
                        ],
                    ]
                },
                "trades": [],
                "asks": [],
                "bids": [],
                "depth": {
                    "type": "depth",
                    "asks": [],
                    "bids": []
                },
                "accounts": []
            }

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('markets/{}'.format(symbol), True)

    def get_order_book(self, symbol):
        """Get symbol market details

        :param symbol: Name of symbol
        :type symbol: str

        .. code:: python

            book = client.get_order_book('ETH-BTC')

        :return: dict

        .. code:: python

            {
                "type": "orderbook",
                "asks": [
                    {
                        "type": "order",
                        "price": "0.06400000",
                        "amount": "0.49499990"
                    },
                    {
                        "type": "order",
                        "price": "0.06500000",
                        "amount": "0.09460000"
                    }
                ],
                "bids": [
                    {
                        "type": "order",
                        "price": "0.01000000",
                        "amount": "1.00000000"
                    },
                    {
                        "type": "order",
                        "price": "0.00100000",
                        "amount": "1.00000000"
                    }
                ]
            }

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('markets/{}/book'.format(symbol), True)

    def get_market_trades(self, symbol):
        """Get symbol market details

        :param symbol: Name of symbol
        :type symbol: str

        .. code:: python

            trades = client.get_market_trades('ETH-BTC')

        :return: list of dicts

        .. code:: python

            [
                {
                  "type": "trade",
                  "trade_id": "fbf447d3-e32f-4458-81ec-de6c73fbc2fb",
                  "trade_side": "BID",
                  "price": "0.06500000",
                  "amount": "0.00000010",
                  "created_at": "2017-10-13T11:42:21.807332899Z"
                }
            ]

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('markets/{}/trades'.format(symbol), True)

    # Order Endpoints

    def create_order(self, symbol, side, price, amount):
        """Create a new order

        :param symbol: Name of symbol
        :type symbol: str
        :param side:  side of order (BID or ASK)
        :type side: str
        :param price: Price as string
        :type price: str
        :param amount: Amount as string
        :type amount: str

        .. code:: python

            order = client.create_order('ETH-BTC', 'BID', '1.0', '1.0')

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {
            'order_market': symbol,
            'order_side': side,
            'price': price,
            'amount': amount
        }

        return self._post('orders', True, data=data)

    def get_orders(self, symbol, limit=None):
        """Get a list of orders

        :param symbol: Name of symbol
        :type symbol: str
        :param limit:  side of order (BID or ASK)
        :type limit: str

        .. code:: python

            orders = client.get_orders('ETH-BTC')

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {
            'market': symbol
        }
        if limit:
            data['limit'] = limit

        return self._get('orders', True, data=data)

    def get_order(self, order_id):
        """Get an order

        :param order_id: Id of order
        :type order_id: str

        .. code:: python

            orders = client.get_order('349b159b-17c5-4f01-8731-f4697a8b439a')

        :return: dict

        .. code:: python

            {
                "type": "order",
                "user_id": "300975cd-4534-49c6-b5cf-921bf4664109",
                "order_id": "1f0b4f9c-ad78-454f-a629-c3a9704f0c83",
                "order_market": "ETH-BTC",
                "order_type": "LIMIT",
                "order_side": "ASK",
                "order_state": "filled",
                "price": "0.001",
                "amount": "1",
                "filled_amount": "0",
                "created_at": "2017-10-15T05:59:02.045166806Z"
            }

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._get('orders/{}'.format(order_id), True)

    def cancel_order(self, order_id):
        """Cancel an order

        :param order_id: Id of order
        :type order_id: str

        .. code:: python

            res = client.cancel_order('349b159b-17c5-4f01-8731-f4697a8b439a')

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        return self._delete('orders/{}'.format(order_id), True)

    def cancel_orders(self, order_ids):
        """Cancel all orders

        :param order_ids: List of order ids
        :type order_ids: list

        .. code:: python

            res = client.cancel_orders([
                "f1d90216-0be5-4258-99a9-6d354815608e",
                "57ae31c2-bcb1-4744-a2aa-6a3f72430699"
            ])

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = [
            {'order_id': oid} for oid in order_ids
        ]

        return self._post('orders/cancel', True, data=data)

    # Trade endpoints

    def get_trades(self, symbol, limit=None, offset=None):
        """Get a list of orders

        :param symbol: Name of symbol
        :type symbol: str
        :param limit: limit of trades
        :type limit: str
        :param offset:  side of order (BID or ASK)
        :type offset: str

        .. code:: python

            trades = client.get_trades('ETH-BTC')

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {
            'market': symbol
        }
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return self._get('trades', True, data=data)

    # Withdraw endpoints

    def withdraw(self, address, currency, amount, fee, currency_pin, label=None):
        """Request a withdrawal

        :param address: Address string e.g '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX'
        :type address: str
        :param currency: Currency to withdraw e.g 'BTC'
        :type address: str
        :param amount: Amount of currency to send
        :type amount: str
        :param fee: Fee to pay? e.g 0.002
        :type amount: str
        :param currency_pin: Pin for the currency
        :type currency_pin: str
        :param label: optional - note about the withdrawal
        :type label: str

        .. code:: python

            withdrawal = client.withdraw(
                '1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX',
                'BTC',
                '0.590464',
                '0.002',
                'your currency pin',
                'some label notes'
            )

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {
            'address': address,
            'withdrawal_type': currency,
            'asset_pin': currency_pin,
            'amount': amount,
            'fee': fee,
            'label': label
        }

        return self._post('withdrawals', True, data=data)

    def get_withdrawals(self, currency=None, limit=None, offset=None):
        """Get a list of withdrawals

        :param currency: optional - Name of currency
        :type currency: str
        :param limit: limit of withdrawals
        :type limit: str
        :param offset:  side of order (BID or ASK)
        :type offset: str

        .. code:: python

            withdrawals = client.get_withdrawals('BTC')

        :return: list of dicts

        .. code:: python

            [
                {
                    "type": "withdrawal",
                    "withdrawal_id": "1170968f-c5a0-4c72-b919-02f2f4b5f2c3",
                    "withdrawal_type": "BTC",
                    "address": "1F1tAaz5x1HUXrCNLbtMDqcw6o5GNn4xqX",
                    "label": "some notes",
                    "amount": "0.59046400",
                    "state": "initial",
                    "scanner_url": "https://blockchain.info/tx/",
                    "created_at": "2017-11-07T10:31:32.911756961Z"
                }
            ]

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {}
        if currency:
            data['currency'] = currency
        else:
            data['currency'] = 'ALL'
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return self._get('withdrawals', True, data=data)

    # Deposit endpoints

    def get_deposits(self, currency=None, limit=None, offset=None):
        """Get a list of deposits

        :param currency: optional - Name of currency
        :type currency: str
        :param limit: limit of withdrawals
        :type limit: str
        :param offset:  side of order (BID or ASK)
        :type offset: str

        .. code:: python

            # get all deposits
            deposits = client.get_deposits()

            # get BTC deposits
            deposits = client.get_deposits('BTC')

        :return: list of dicts

        .. code:: python

            [
                {
                    "type": "deposit",
                    "deposit_id": "7b76603c-db87-4c4a-b36f-9981058d885e",
                    "deposit_type": "ETH",
                    "amount": "1.00000000",
                    "confirmations": 2231,
                    "state": "confirmed",
                    "scanner_url": "https://etherscan.io/tx/0x181a1d616b5b07d5a404636c527ca5432878664d4b85a20976bbd72c07e58abe",
                    "created_at": "2017-09-06T07:53:41.297047856Z"
                }
            ]

        :raises:  BigoneResponseException, BigoneAPIException

        """

        data = {}
        if currency:
            data['currency'] = currency
        else:
            data['currency'] = 'ALL'
        if limit:
            data['limit'] = limit
        if offset:
            data['offset'] = offset

        return self._get('withdrawals', True, data=data)
