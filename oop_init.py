#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse
from parser_xlsx_adventa import main

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', default='мир')
    parser.add_argument('-a', '--adr', default='')

    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])



    # print (namespace)

    print("Namespace, {}!".format(namespace))
    print("Привет, {}!".format(namespace.name))
    print("Адрес, {}!".format(namespace.adr))
    main(namespace.adr)