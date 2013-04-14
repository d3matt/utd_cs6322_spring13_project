#!/bin/bash

REPOS="J P N E S A D W C H I L O Y "
OPTIONS="--no-host-directories --recursive --no-parent --timestamping"
YEARS="00 01 02 03 04 05 06 07 08 09 10 11 12 13"

for repo in $REPOS ; do
    for year in $YEARS ; do
        url="http://www.aclweb.org/anthology-new/${repo}/${repo}${year}/"
        echo -e "\n\n\nCrawling: $url\n\n\n"
        wget ${OPTIONS} $url
    done
done

./genFiles.py
