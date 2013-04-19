#!/usr/bin/env python

import os

bad = []
for line in open("BAD").readlines():
    line = line.strip()
    if line:
        bad.append(line)
make = open("Files.make", "w")

def callback(arg, dirname, files):
    for file in files:
        if '.pdf' in file:
            fullfile = "%s/%s" % (dirname, file)
            if fullfile not in bad:
                make.write("files: ")
                make.write(fullfile.replace('.pdf', '.cxml'))
                make.write(' ')
                make.write(fullfile.replace('.pdf', '.hxml'))
                make.write('\n')

os.path.walk("anthology-new", callback, None)
