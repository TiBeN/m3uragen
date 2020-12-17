#!/usr/bin/env python3
#
# args: <inpath> <outpath>

from pathlib import Path
import sys
import zipfile
import os.path

# function create m3u (output path, name, files)


def create_m3u(outpath, name, files):

    m3ufile = open(str(outpath) + '/' + name + '.m3u', 'w')
    for i in files:
        imgpath = os.path.relpath(i, outpath)
        m3ufile.write(imgpath + '\n')

    m3ufile.close()


# Process arguments

if len(sys.argv) != 3:
    sys.stderr('ERROR: Bad number of arguments')
    sys.exit(-1)

inpath = Path(sys.argv[1]).resolve()
outpath = Path(sys.argv[2]).resolve()

# Some input checks

if not inpath.is_dir():
    sys.stderr.write(f'ERROR: Directory does not exists: {inpath}\n')
    sys.exit(-1)

# Create output collection directory tree

outimgpath = Path(str(outpath) + '/img')
outm3upath = Path(str(outpath) + '/m3u')

try:
    for i in [outimgpath, outm3upath]:
        i.mkdir(parents=True)
except FileExistsError:
    sys.stderr.write(f'ERROR: Directory exists: {i}\n')
    sys.exit(-1)

# Iterate accross zip files in inpath

infiles = list(inpath.iterdir())

for i in infiles:
    print(f'Process {i.name}')

    if not zipfile.is_zipfile(i):
        print(f'{i.name} is not a zip file: discard')
        continue

    zfile = zipfile.ZipFile(i)
    zcontents = zfile.infolist()
    name = Path(i).stem
    imgs = []

    for j in zcontents:
        zfile.extract(j, outimgpath)
        imgs.append(outimgpath / j.filename)

    imgs.sort()

    if len(imgs) > 1:
        create_m3u(outm3upath, name, imgs)

