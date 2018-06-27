# coding=utf-8

from bigone.client import Client
from bigone.exceptions import BigoneAPIException, BigoneRequestException
import pytest
import requests_mock


client = Client('api_key', 'api_secret')


def test_invalid_json():
    """Test Invalid response Exception"""

    with pytest.raises(BigoneRequestException):
        with requests_mock.mock() as m:
            m.get('https://big.one/api/v2/markets', text='<head></html>')
            client.get_markets()


def test_api_exception():
    """Test API response Exception"""

    with pytest.raises(BigoneAPIException):
        with requests_mock.mock() as m:
            json_obj = {
                'errors': [{
                    'code': 20102,
                    'message': 'Unsupported currency ABC'
                }]
            }
            m.get('https://big.one/api/v2/accounts/ABC', json=json_obj, status_code=422)
            client.get_account('ABC')
