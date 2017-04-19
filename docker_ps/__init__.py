#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import print_function

import sys
import pipes
import getopt
import docker

from tabulate import tabulate

__version__ = '0.1.4'

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

    def _port_str(p):
        (pport,c)=p
        return '(' + '/'.join(map(lambda c: '{ip}:{port}'.format(ip=c['HostIp'],
            port=c['HostPort']), c)) + ') <- ' + pport

    t = []
    for container in cli.containers.list(all=True):
        t.append([
            container.name,
            container.attrs['Config']['Image'],
            ', '.join(map(_port_str, container.attrs['NetworkSettings']['Ports'].iteritems())),
            container.status
        ])
    print(tabulate(t, headers=['CONTAINER', 'IMAGE', 'PORTS', 'STATUS']))
    print()

if __name__ == "__main__":
    main()

