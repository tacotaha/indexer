# Indexer
> A multithreaded inverted indexer for a generic set of documents

## Description
Given a set of documents, the indexer will create a directory by the name of
```index``` containing a file for every term in the corpus. Within each file is a
[pickled](https://docs.python.org/3/library/pickle.html) list of tupples of the form 
(f, d) where f is the frequency of the term in the document d.
 
## Installation

```
  $ git clone https://github.com/tazzaoui/indexer.git && cd indexer
  $ pip install -r requirements.txt
```

## Usage

```
usage: main.py [-h] [-p PATH] [-t THREADS]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  Document path
  -t THREADS, --threads THREADS
                        Number of threads to launch
```

Example: ```./main.py -p /some/document/path -t 10```
