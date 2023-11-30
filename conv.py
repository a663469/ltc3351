#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import argv

script, file_dump = argv

# dump = open(file_dump, "r")
# Lines = dump.readlines()
# for line in Lines:
#     words = line.split()
#     match words:
#         case 0x00:

#     # print(words[0] + " " + words[1])

for var in register_map:
    print(var)
