#! /usr/bin/python3

# Implement a web request interface to interact with Ricequant.

from requests import Request, Session, exceptions
import re, json

from . import file

headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'zh,zh-CN;q=0.7,en-US;q=0.3',
        # 'Referer': rqConfig.rqEndpointUrl,
        'X-Requested-With': 'XMLHttpRequest',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }

def prepareGenericRequest(urlRoute, urlParams, headers, method, sensitive=True):
    webRequest = Request(method, urlRoute, params=urlParams, headers=headers)
    session = Session()
    sess = session.prepare_request(webRequest)
    
    resp = session.send(sess) # 发报

    return resp

