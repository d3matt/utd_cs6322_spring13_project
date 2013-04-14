#!/bin/bash

echo -n > Files.make

for file in $(find . -name *.pdf | sed 's/\.pdf//' ) ; do
    echo "files: ${file}.cxml ${file}.hxml" >> Files.make
done
