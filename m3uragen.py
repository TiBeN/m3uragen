#!/usr/bin/env python3

from pathlib import Path
import sys
import re

# Process arguments

if len(sys.argv) < 3:
    sys.stderr('ERROR: bad number of arguments')
    sys.exit(-1)

coldir = Path(sys.argv[1]).resolve()
m3udir = Path(sys.argv[2]).resolve()
patterns = sys.argv[3:]

# Iter sub folders and folder as final folder
#
# Filter list: items that contains the regex
# Sort list
#
# for each item
#   (refer to algo in readme)

if not coldir.is_dir():
    sys.stderr.write(f'ERROR: Directory does not exists: {coldir}\n')
    sys.exit(-1)


def createm3u(imgset):
    print(imgset)


def process_dir(dir):
    print(f'Process directory: {dir}')
    imgfiles = []
    for path in dir.iterdir():
        if not path.is_file():
            continue
        imgfiles.append(str(path))
    imgfiles.sort()
    appimgset = []
    cur_appname = ''
    for imgfile in imgfiles:
        pattern = re.compile('.*(' + patterns[0] + ').*')
        match = pattern.match(imgfile)
        if match:
            multiparts_str = match.group(1)
            img_appname = imgfile.replace(multiparts_str, '')
            if img_appname != cur_appname and len(appimgset) > 0:
                createm3u(appimgset)
                appimgset.clear()

            appimgset.append(imgfile)
            cur_appname = img_appname


def scan_dirs(dir):

    for path in dir.iterdir():
        if path.is_dir():
            scan_dirs(path)
            process_dir(path)


scan_dirs(coldir)

