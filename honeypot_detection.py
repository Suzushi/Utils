#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import socket
import socks
from lib.socks_resolver.engine import getaddrinfo
from lib.payload.scanner.service.engine import recv_all


# 蜜獾检测


def conn(targ, port, timeout_sec, socks_proxy):
    """
    socket连接方法
    Args:
        targ: 目标主机
        port: 目标端口
        timeout_sec: 超时时间
        socks_proxy: socks代理
    Returns:
        s: python socket
    """
    try:
        if socks_proxy is not None:
            socks_version = socks.SOCKS5 if socks_proxy.startswith(
                'socks5://') else socks.SOCKS4
            socks_proxy = socks_proxy.rsplit('://')[1]
            if '@' in socks_proxy:
                socks_username = socks_proxy.rsplit(':')[0]
                socks_password = socks_proxy.rsplit(':')[1].rsplit('@')[0]
                socks.set_default_proxy(socks_version, str(socks_proxy.rsplit('@')[1].rsplit(':')[0]),
                                        int(socks_proxy.rsplit(':')[-1]), username=socks_username,
                                        password=socks_password)
                socket.socket = socks.socksocket
                socket.getaddrinfo = getaddrinfo
            else:
                socks.set_default_proxy(socks_version, str(socks_proxy.rsplit(':')[0]),
                                        int(socks_proxy.rsplit(':')[1]))
                socket.socket = socks.socksocket
                socket.getaddrinfo = getaddrinfo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sys.stdout.flush()
        s.settimeout(timeout_sec)
        s.connect((targ, port))
        return s
    except Exception:
        return None


def kippo_detect(host, port, timeout=None, socks_proxy=None):
    try:
        s = conn(host, port, timeout, socks_proxy)
        spacer = '\r\n'
        if s is not None:
            banner = recv_all(s)
            s.send(banner + spacer)
            response = recv_all(s)
            if ('Protocol mismatch' in response or 'bad packet length' in response):
                return True
            else:
                return False
        else:
            return False
    except Exception:
        return False
