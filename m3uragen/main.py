"""
m3uragen main entry point
"""

from pathlib import Path
from romset import ZipRomSet, NonZipRomSet
import m3u
import logging


def _parseargs():
    # Handle argument parsing here 
    # Now use a raw options dict to implement logic first

    zipopts = {
        'is_zipped': True,
        'scan_subdirs': False,
        'suffix': None,
        'image_extensions': None,
        'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/no-intro-c64').resolve(),
        # 'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/recur-zip').resolve(),
        'unzip_dir': Path('/home/ben/src/m3uragen/tmp/output/c64/img'),
        'm3u_dir': Path('/home/ben/src/m3uragen/tmp/output/c64/m3u'),
        'verbose': True
    }

    # nonzipopts = {
    #     'is_zipped': False,
    #     'scan_subdirs': True,
    #     'media_flag_pattern': ' - (Disk|Side) [A-Z0-9]+[^.]*',
    #     'image_extensions': ['dsk'],
    #     'suffix': ' (dsk)',
    #     'romset_dir': Path('/home/ben/src/m3uragen/tmp/nonzipset/gamebasecpc').resolve(),
    #     # 'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/recur-zip').resolve(),
    #     'm3u_dir': Path('/home/ben/src/m3uragen/tmp/output/cpc/m3u'),
    #     'verbose': True
    # }

    # nonzipopts = {
    #    'is_zipped': False,
    #    'scan_subdirs': True,
    #    'media_flag_pattern': '\\(Disk \\d+ of \\d+\\)',
    #    'image_extensions': None,
    #    'romset_dir': Path('/home/ben/src/m3uragen/tmp/nonzipset/new-tosec-atarist').resolve(),
    #    # 'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/recur-zip').resolve(),
    #    'm3u_dir': Path('/home/ben/src/m3uragen/tmp/output/st'),
    #     'verbose': True
    #}

    return zipopts
    

def _main(opts):

    logging.basicConfig(format='%(levelname)s:%(message)s', 
                        level=logging.INFO if opts['verbose'] else logging.WARNING)

    if opts['is_zipped']:
        romset = ZipRomSet(opts['romset_dir'], opts['scan_subdirs'])
        romset.unzip_images_to(opts['unzip_dir'])
    else:
        romset = NonZipRomSet(opts['romset_dir'], opts['scan_subdirs'], 
                              opts['media_flag_pattern'], opts['image_extensions'])
    m3u.generate_all(romset.multi_images_softwares(), opts['m3u_dir'], opts['suffix'])


if __name__ == '__main__':
    _main(_parseargs())
