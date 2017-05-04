#!/usr/bin/env python
import sys

from utils import update_index

if __name__ == '__main__':
    new_item = sys.argv[1]
    update_index(new_item)
