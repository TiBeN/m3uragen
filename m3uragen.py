#!/usr/bin/env python3

from pathlib import Path
import sys
import re
import os


def create_m3u(outpath, name, files):
    m3ufile = str(outpath) + '/' + name + '.m3u'
    print(f'Write: {m3ufile}')
    resource = open(m3ufile, 'w')
    for i in files:
        imgpath = os.path.relpath(i, outpath)
        resource.write(imgpath + '\n')
    resource.close()


def process_dir(dir, m3udir):
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
                name = Path(cur_appname).name
                create_m3u(m3udir, name, appimgset)
                appimgset.clear()
            appimgset.append(imgfile)
            cur_appname = img_appname


def scan_dirs(dir, m3udir):

    for path in dir.iterdir():
        if path.is_dir():
            scan_dirs(path, m3udir)
            process_dir(path, m3udir)


# Process arguments

if len(sys.argv) < 3:
    sys.stderr('ERROR: bad number of arguments')
    sys.exit(-1)

# Check and prepare directories

coldir = Path(sys.argv[1]).resolve()
m3udir = Path(sys.argv[2]).resolve()
patterns = sys.argv[3:]

if not coldir.is_dir():
    sys.stderr.write(f'ERROR: Directory does not exists: {coldir}\n')
    sys.exit(-1)

m3udir.mkdir(parents=True)    

scan_dirs(coldir, m3udir)
