#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket


def get_addr_info(*args):
    """
    使用socks代理解析地址

    Args:
        args: *args

    Returns:
        socks.getaddrinfo
    """
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
