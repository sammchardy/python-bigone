# coding=utf-8


class BigoneAPIException(Exception):
    """Exception class to handle general API Exceptions

        `code` values

        `message` format

    """
    def __init__(self, response):
        self.code = ''
        self.message = 'Unknown Error'
        try:
            json_res = response.json()
        except ValueError:
            print("Can't parse error response: {}".format(response.text))
            self.message = response.text
        else:
            print("doing something with json_res: {}".format(json_res))
            if 'msg' in json_res:
                self.message = json_res['msg']
                self.code = json_res['code']
            elif 'errors' in json_res:
                if type(json_res['errors']) == list:
                    self.message = "\n ".join(["{}: {}".format(el['code'], el['message']) for el in json_res['errors']])
                elif 'detail' in json_res['errors']:
                    self.message = json_res['errors']['detail']

        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):
        return 'BigoneAPIException {}: {}'.format(self.code, self.message)


class BigoneRequestException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return 'BigoneRequestException: {}'.format(self.message)
