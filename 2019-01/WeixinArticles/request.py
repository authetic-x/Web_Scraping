from config import *
from requests import Request

class WeixinRequest(Request):
    def __init__(self, url, method='GET', headers=None, callback=None, need_proxy=None,
                 timeout=TIMEOUT, failed_time=0):
        Request.__init__(self, method, url, headers)
        self.need_proxy = need_proxy
        self.callback = callback
        self.failed_time = failed_time
        self.timeout = timeout