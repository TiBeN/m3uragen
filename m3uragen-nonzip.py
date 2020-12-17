#!/usr/bin/env python3

from pathlib import Path
import sys
import re
import os


def create_m3u(outpath, name, files):
    m3ufile = str(outpath) + '/' + name + '.m3u'
    print(f'Write: {m3ufile}')
    resource = open(m3ufile, 'w')
    files.sort()
    for i in files:
        imgpath = os.path.relpath(i, outpath)
        resource.write(imgpath + '\n')
    resource.close()


def remove_media_flag(img_file, pattern):
    match = pattern.match(img_file)
    if match:
        media_flag = match.group(1)
        return img_file.replace(media_flag, '')
    else:
        print(f'No match {img_file}')


def process_dir(dir, m3udir):
    print(f'Process directory: {dir}')

    imgs_dict = dict()
    media_flag_pattern = re.compile('.*(' + patterns[0] + ').*')
    for item in dir.iterdir():
        if not item.is_file():
            continue
        img_file_without_media_flag = remove_media_flag(str(item), media_flag_pattern)
        if img_file_without_media_flag not in imgs_dict:
            imgs_dict[img_file_without_media_flag] = []
        imgs_dict[img_file_without_media_flag].append(item)

    for i, img_files in imgs_dict.items():
        if i is None:
            continue
        softname = Path(Path(i).stem).name
        print(softname)
        create_m3u(m3udir, softname, img_files)


def scan_dirs(dir, m3udir):

    for path in dir.iterdir():
        if path.is_dir():
            scan_dirs(path, m3udir)
    process_dir(dir, m3udir)

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
