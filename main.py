#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from argparse import ArgumentParser
from indexer import Indexer

def main():
    parser = ArgumentParser()
    parser.add_argument("-p", "--path", dest="path", default=None,
                        help="Document path")
    parser.add_argument("-t", "--threads", dest="threads",
                        help="Number of threads to launch")
    args = parser.parse_args()
    path = os.path.abspath(args.path) if args.path else "docs"
    threads = int(args.threads) if args.threads else 5
    indexer = Indexer(path, threads)
    indexer.create_index()

if __name__ == "__main__":
    main()
