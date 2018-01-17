# coding=utf-8

from bigone.client import Client
from bigone.exceptions import BigoneAPIException, BigoneRequestException
import pytest
import requests_mock


client = Client('api_key')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(BigoneRequestException):
        with requests_mock.mock() as m:
            m.get('https://api.big.one/markets', text='<head></html>')
            client.get_markets()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(BigoneAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                'error': {
                    'status': 422,
                    'code': 20102,
                    'description': 'Unsupported currency ABC'
                }
            }
            m.get('https://api.big.one/accounts/ABC', json=json_obj, status_code=422)
            client.get_account('ABC')
