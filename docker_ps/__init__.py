#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import sys
import pipes
import getopt

from tabulate import tabulate
from docker import Client

__version__ = '0.1.0'

def main():

    cli = Client()

    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], "v")
    except getopt.GetoptError as _:
        print("Usage: docker-ps [-v]")
        sys.exit(2)

    for opt, _ in opts:
        if opt == '-v':
            print(__version__)
            sys.exit()

    def _port_str(c):
        if c['PublicPort'] == c['PrivatePort']:
            return '{ip}:{port}'.format(ip=c['IP'], port=c['PublicPort'])
        else:
            return '{ip}:{port} <- {pport}'.format(ip=c['IP'], 
                port=c['PublicPort'], pport=c['PrivatePort'])

    t = []
    for container in cli.containers():
        t.append([
            ', '.join(map(lambda c: c[1:], container['Names'])),
            container['Image'],
            ', '.join(map(_port_str, container['Ports'])),
            container['Status']
        ])
    print(tabulate(t, headers=['CONTAINER', 'IMAGE', 'PORTS', 'STATUS']))
    print()

if __name__ == "__main__":
    main()

