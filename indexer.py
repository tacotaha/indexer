#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
This file contains the implementation of the indexer.
Given a set of documents, the indexer will create a
directory by the name of 'index' containing a file for
every term in the corpus. Within that file is a pickled
list of tupples of the form (f, d) where f is the frequency
of the term in the document d
"""

import os
import base64
import pickle
import logging
import threading
from support.token_extract import extract_tokens

class Indexer:
    def __init__(self, path=None, threads=5):
        self.logger = logging.getLogger("indexer")
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler("indexer.log")
        fh.setFormatter(logging.Formatter('%(asctime)s - \
            %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(fh)
        self.path = os.path.abspath(path)
        self.threads = threads
        self.lock = threading.Lock()

    def create_index(self):
        """
        This method launches each thread for indexing
        """
        os.system("rm -rf index; mkdir -p index")
        threads = list()
        for tid in range(self.threads):
            thread = threading.Thread(target=self.__launch, args=[tid])
            self.logger.info("Launched thread {}".format(tid))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

    def __launch(self, tid):
        """
        This is the threaded method that performs the indexing
        """
        assert os.path.isdir(self.path), "Nonexistent document directory"
        document_dir = os.fsencode(self.path)
        count = 0
        document_count = len(os.listdir(document_dir))
        start_index = (tid*document_count) // self.threads
        if tid == self.threads - 1:
            end_index = document_count - 1
        else:
            end_index = ((tid+1)*document_count) // self.threads - 1
        for document in os.listdir(document_dir)[start_index:end_index]:
            file_name = os.fsdecode(document)
            tokens = extract_tokens(os.path.join(self.path, file_name))
            for (freq, tok) in tokens:
                file_name = os.path.join(b"index", base64.b16encode(tok.encode()))
                with self.lock:
                    try:
                        f = open(file_name, "rb")
                        token = pickle.load(f)
                        f.close()
                    except IOError as e:
                        token = []
                    token.append((freq, document))
                    try:
                        token_file = open(file_name, "wb")
                        pickle.dump(token, token_file)
                        token_file.close()
                    except Exception as e:
                        self.logger.info("[{}]: {}".format(tid, e))
            if count  % 1000 == 0:
                self.logger.info("[%d]: indexed %d/%d", tid, count, end_index-start_index)
            count += 1

    def __del__(self):
        self.logger.info("Object destroyed")
