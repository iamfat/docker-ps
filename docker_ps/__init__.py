#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import sys
import pipes
import getopt
import docker

from tabulate import tabulate

__version__ = '0.1.3'

def main():

    cli = docker.from_env()

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
        if 'PublicPort' not in c:
            return '{pport}'.format(pport=c['PrivatePort'])
        elif c['PublicPort'] == c['PrivatePort']:
            return '{ip}:{port}'.format(ip=c['IP'], port=c['PublicPort'])
        else:
            return '{ip}:{port}>{pport}'.format(ip=c['IP'],g
                port=c['PublicPort'], pport=c['PrivatePort'])

    t = []
    for container in cli.containers.list(all=True):
        t.append([
            ', '.join(map(lambda c: c[1:], container.attrs['Names'])),
            container.attrs['Image'],
            ', '.join(map(_port_str, container.attrs['Ports'])),
            container.attrs['Status']
        ])
    print(tabulate(t, headers=['CONTAINER', 'IMAGE', 'PORTS', 'STATUS']))
    print()

if __name__ == "__main__":
    main()

