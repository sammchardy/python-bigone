# coding=utf-8

import jwt
import requests
import time

from .exceptions import BigoneAPIException, BigoneRequestException


class Client(object):

    API_URL = 'https://big.one/api/v2'

    SIDE_BID = 'BID'
    SIDE_ASK = 'ASK'

    def __init__(self, api_key, api_secret):
        """Big.One API Client constructor

        https://open.big.one/

        :param api_key: Api Key
        :type api_key: str
        :param api_key: Api Secret
        :type api_key: str

        .. code:: python

            client = Client(api_key, api_secret)

        """

        self.API_KEY = api_key
        self.API_SECRET = api_secret
        self.session = self._init_session()

    def _init_session(self):

        session = requests.session()
        headers = {'Accept': 'application/json',
                   'User-Agent': 'python-bigone'}
        session.headers.update(headers)
        return session

    def _create_uri(self, path):
        return '{}/{}'.format(self.API_URL, path)

    def _create_signature(self, ):

        headers = {'typ': 'JWT', 'alg': 'HS256'}
        payload = {
            'type': 'OpenAPI',
            'sub': self.API_KEY,
            'nonce': int(time.time() * 1000000000)  # convert to nanoseconds
        }
        sig = jwt.encode(payload, self.API_SECRET, algorithm='HS256', headers=headers)
        return sig.decode("utf-8")

    def _request(self, method, path, signed, **kwargs):

        data = kwargs.get('data', None)

        if signed:
            kwargs['headers'] = {
                'Authorization': 'Bearer {}'.format(self._create_signature())
            }

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

            if 'msg' in json or 'errors' in json:
                raise BigoneAPIException(response)

            # by default return full response
            res = json
            # if it's a normal response we have a data attribute, return that
            if 'data' in json:
                res = json['data']
            return res
        except ValueError:
            raise BigoneRequestException('Invalid Response: {}'.format(response.text))

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

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('viewer/accounts', True)

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

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('accounts/{}'.format(currency), True)

    # Market endpoints

    def get_markets(self):
        """List markets

        https://open.big.one/docs/api_market.html#all-markets

        .. code:: python

            markets = client.get_markets()

        :return: list of dicts

        .. code:: python

            [
                {
                    "uuid": "d2185614-50c3-4588-b146-b8afe7534da6",
                    "quoteScale": 8,
                    "quoteAsset": {
                        "uuid": "0df9c3c3-255a-46d7-ab82-dedae169fba9",
                        "symbol": "BTC",
                        "name": "Bitcoin"
                    },
                    "name": "BTG/BTC",
                    "baseScale": 4,
                    "baseAsset": {
                        "uuid": "5df3b155-80f5-4f5a-87f6-a92950f0d0ff",
                        "symbol": "BTG",
                        "name": "Bitcoin Gold"
                    }
                }
            ]

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('markets')

    def get_tickers(self):
        """List market tickers

        https://open.big.one/docs/api_tickers.html#tickers-of-all-market

        .. code:: python

            markets = client.get_tickers()

        :return: list of dicts

        .. code:: python

            [
                {
                    "volume": null,
                    "open": "1.0000000000000000",
                    "market_uuid": "ETH-EOS",
                    "low": null,
                    "high": null,
                    "daily_change_perc": "0",
                    "daily_change": "0E-16",
                    "close": "1.0000000000000000",
                    "bid": {
                        "price": "1.0000000000000000",
                        "amount": "106.0000000000000000"
                    },
                    "ask": {
                        "price": "45.0000000000000000",
                        "amount": "4082.3283464000000000"
                    }
                }
            ]

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('tickers')

    def get_ticker(self, symbol):
        """Get symbol market details

        https://open.big.one/docs/api_tickers.html#ticker-of-one-market

        :param symbol: Name of symbol
        :type symbol: str

        .. code:: python

            # using market ID
            market = client.get_ticker('ETH-BTC')

            # using market UUID
            market = client.get_ticker('d2185614-50c3-4588-b146-b8afe7534da6')

        :return: dict

        .. code:: python

            {
                "volume": null,
                "open": "42.0000000000000000",
                "market_uuid": "BTC-EOS",
                "low": "42.0000000000000000",
                "high": null,
                "daily_change_perc": "0",
                "daily_change": "0E-16",
                "close": "42.0000000000000000",
                "bid": {
                    "price": "42.0000000000000000",
                    "amount": "3.3336371100000000"
                },
                "ask": {
                    "price": "45.0000000000000000",
                    "amount": "4082.3283464000000000"
                }
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('markets/{}/ticker'.format(symbol))

    def get_order_book(self, symbol):
        """Get symbol market details

        :param symbol: Name of symbol
        :type symbol: str

        .. code:: python

            # Using market ID
            book = client.get_order_book('ETH-BTC')

            # Using market UUID
            book = client.get_order_book('d2185614-50c3-4588-b146-b8afe7534da6')

        :return: dict

        .. code:: python

            {
                "market_uuid": "BTC-EOS",
                "bids": [
                    {
                        "price": "42",
                        "order_count": 4,
                        "amount": "23.33363711"
                    }
                ],
                "asks": [
                    {
                        "price": "45",
                        "order_count": 2,
                        "amount": "4193.3283464"
                    }
                ]
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('markets/{}/depth'.format(symbol))

    def get_market_trades(self, symbol, after=None, before=None, first=None, last=None):
        """Get market trades - max 50

        https://open.big.one/docs/api_market_trade.html#trades-of-a-market

        :param symbol: Name of symbol
        :type symbol: str
        :param after: Return trades after this id
        :type after: int
        :param before: Return trades before this id
        :type before: int
        :param first: Slicing count
        :type first: int
        :param last: Slicing count
        :type last: int

        .. code:: python

            trades = client.get_market_trades('ETH-BTC')

            # using after trade ID
            trades = client.get_market_trades('ETH-BTC', after=1)

            # using first slice value
            trades = client.get_market_trades('ETH-BTC', first=20)

        :return: list of dicts

        .. code:: python

            {
                "edges": [
                    {
                        "node": {
                            "taker_side": "BID",
                            "price": "46.1450000000000000",
                            "market_uuid": "BTC-EOS",
                            "id": 1,
                            "amount": "0.2465480000000000"
                        },
                        "cursor": "dGVzdGN1cmVzZQo="
                    }
                ],
                "page_info": {
                "end_cursor": "dGVzdGN1cmVzZQo=",
                "start_cursor": "dGVzdGN1cmVzZQo=",
                "has_next_page": true,
                "has_previous_page": false
                }
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """
        data = {}
        if after:
            data['after'] = after
        if before:
            data['before'] = before
        if first:
            data['first'] = first
        if last:
            data['last'] = last

        return self._get('markets/{}/trades'.format(symbol), data=data)

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

            {
                "id": 10,
                "market_uuid": "BTC-EOS",
                "price": "10.00",
                "amount": "10.00",
                "filled_amount": "9.0",
                "avg_deal_price": "12.0",
                "side": "ASK",
                "state": "FILLED"
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        data = {
            'market_id': symbol,
            'side': side,
            'price': price,
            'amount': amount
        }

        return self._post('viewer/orders', True, data=data)

    def get_orders(self, symbol, after=None, before=None, first=None, last=None, side=None, state=None):
        """Get a list of orders

        :param symbol: Name of symbol
        :type symbol: str
        :param after: Return trades after this id
        :type after: int
        :param before: Return trades before this id
        :type before: int
        :param first: Slicing count
        :type first: int
        :param last: Slicing count
        :type last: int
        :param side: Order Side ASK|BID
        :type side: str
        :param state: Order State CANCELED|FILLED|PENDING
        :type state: str

        .. code:: python

            orders = client.get_orders('ETH-BTC')

        :return: dict

        .. code:: python

            {
                "edges": [
                    {
                        "node": {
                            "id": 10,
                            "market_uuid": "d2185614-50c3-4588-b146-b8afe7534da6",
                            "price": "10.00",
                            "amount": "10.00",
                            "filled_amount": "9.0",
                            "avg_deal_price": "12.0",
                            "side": "ASK",
                            "state": "FILLED"
                        },
                        "cursor": "dGVzdGN1cmVzZQo="
                    }
                ],
                "page_info": {
                    "end_cursor": "dGVzdGN1cmVzZQo=",
                    "start_cursor": "dGVzdGN1cmVzZQo=",
                    "has_next_page": true,
                    "has_previous_page": false
                }
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        data = {
            'market_id': symbol
        }
        if after:
            data['after'] = after
        if before:
            data['before'] = before
        if first:
            data['first'] = first
        if last:
            data['last'] = last
        if side:
            data['side'] = side
        if state:
            data['state'] = state

        return self._get('viewer/orders', True, data=data)

    def get_order(self, order_id):
        """Get an order

        https://open.big.one/docs/api_orders.html#get-one-order

        :param order_id: Id of order
        :type order_id: str

        .. code:: python

            orders = client.get_order('10')

        :return: dict

        .. code:: python

            {
                "id": 10,
                "market_uuid": "d2185614-50c3-4588-b146-b8afe7534da6",
                "price": "10.00",
                "amount": "10.00",
                "filled_amount": "9.0",
                "avg_deal_price": "12.0",
                "side": "ASK",
                "state": "FILLED"
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._get('viewer/orders/{}'.format(order_id), True)

    def cancel_order(self, order_id):
        """Cancel an order

        https://open.big.one/docs/api_orders.html#cancle-order

        :param order_id: Id of order
        :type order_id: str

        .. code:: python

            res = client.cancel_order('10')

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._post('viewer/orders/{}/cancel'.format(order_id), True)

    def cancel_orders(self):
        """Cancel all orders

        https://open.big.one/docs/api_orders.html#cancle-all-orders


        .. code:: python

            res = client.cancel_orders()

        :return: dict

        .. code:: python

            {}

        :raises:  BigoneRequestException, BigoneAPIException

        """

        return self._post('viewer/orders/cancel_all', True)

    # Trade endpoints

    def get_trades(self, symbol=None, after=None, before=None, first=None, last=None):
        """Get a list of your trades

        :param symbol: Name of symbol
        :type symbol: str
        :type after: int
        :param before: Return trades before this id
        :type before: int
        :param first: Slicing count
        :type first: int
        :param last: Slicing count
        :type last: int

        .. code:: python

            trades = client.get_trades('ETH-BTC')

        :return: dict

        .. code:: python

            {
                "edges": [
                    {
                        "node": {
                            "viewer_side": "ASK" // ASK, BID, SELF_TRADING
                            "taker_side": "BID",
                            "price": "46.1450000000000000",
                            "market_uuid": "BTC-EOS",
                            "id": 1,
                            "amount": "0.2465480000000000"
                        },
                        "cursor": "dGVzdGN1cmVzZQo="
                    }
                ],
                "page_info": {
                    "end_cursor": "dGVzdGN1cmVzZQo=",
                    "start_cursor": "dGVzdGN1cmVzZQo=",
                    "has_next_page": true,
                    "has_previous_page": false
                }
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        data = {}
        if symbol:
            data['market_id'] = symbol
        if after:
            data['after'] = after
        if before:
            data['before'] = before
        if first:
            data['first'] = first
        if last:
            data['last'] = last

        return self._get('viewer/trades', True, data=data)

    # Withdraw endpoints

    def withdrawals(self, first=None, after=None):
        """Get a list of withdrawals

        https://open.big.one/docs/api_withdrawal.html#get-withdrawals-of-user

        :param first: Slicing count
        :type first: str
        :param after: Return withdrawals after this value
        :type after: str

        .. code:: python

            withdrawal = client.withdrawals()

        :return: dict

        .. code:: python

            {
                "edges": [
                    {
                        "node": {
                            "id": 10,
                            "customer_id": "ETH",
                            "asset_uuid": "ETH",
                            "amount": "5",
                            "state": "CONFIRMED",
                            "note": "2018-03-15T16:13:45.610463Z",
                            "txid": "0x4643bb6b393ac20a6175c713175734a72517c63d6f73a3ca90a15356f2e967da0",
                            "completed_at": "2018-03-15T16:13:45.610463Z",
                            "inserted_at": "2018-03-15T16:13:45.610463Z",
                            "is_internal": true,
                            "target_address": "0x4643bb6b393ac20a6175c713175734a72517c63d6f7"
                        },
                        "cursor": "dGVzdGN1cmVzZQo="
                    }
                ],
                "page_info": {
                    "end_cursor": "dGVzdGN1cmVzZQo=",
                    "start_cursor": "dGVzdGN1cmVzZQo=",
                    "has_next_page": true,
                    "has_previous_page": false
                }
            }

        :raises:  BigoneRequestException, BigoneAPIException

        """

        data = {}
        if after:
            data['after'] = after
        if first:
            data['first'] = first

        return self._get('viewer/withdrawals', True, data=data)

    # Deposit endpoints

    def get_deposits(self, first=None, after=None):
        """Get a list of deposits

        https://open.big.one/docs/api_deposit.html#deposit-of-user

        :param first: Slicing count
        :type first: str
        :param after: Return withdrawals after this value
        :type after: str

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

        :raises:  BigoneRequestException, BigoneAPIException

        """

        data = {}
        if after:
            data['after'] = after
        if first:
            data['first'] = first

        return self._get('viewer/deposits', True, data=data)
