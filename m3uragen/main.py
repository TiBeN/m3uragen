"""
m3uragen main entry point
"""

from pathlib import Path
from romset import ZipRomSet, NonZipRomSet
import m3u


def _parseargs():
    # Handle argument parsing here 
    # Now use a raw options dict to implement logic first

    # Zipped list
    # zipopts = {
    #     'is_zipped': True,
    #     'scan_subdirs': False,
    #     'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/no-intro-c64').resolve(),
    #     # 'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/recur-zip').resolve(),
    #     'unzip_dir': Path('/home/ben/src/m3uragen/tmp/output/c64/img'),
    #     'm3u_dir': Path('/home/ben/src/m3uragen/tmp/output/c64/m3u')
    # }

    nonzipopts = {
        'is_zipped': False,
        'scan_subdirs': True,
        'media_flag_pattern': ' - (Disk|Side) [A-Z0-9]+[^.]*',
        'image_extensions': ['cdt'],
        'romset_dir': Path('/home/ben/src/m3uragen/tmp/nonzipset/gamebasecpc').resolve(),
        # 'romset_dir': Path('/home/ben/src/m3uragen/tmp/zipset/recur-zip').resolve(),
        'm3u_dir': Path('/home/ben/src/m3uragen/tmp/output/cpc/m3u')
    }

    return nonzipopts
    

def _main(opts):
    if opts['is_zipped']:
        romset = ZipRomSet(opts['romset_dir'], opts['scan_subdirs'])
        romset.unzip_images_to(opts['unzip_dir'])
    else:
        romset = NonZipRomSet(opts['romset_dir'], opts['scan_subdirs'], 
                              opts['media_flag_pattern'], opts['image_extensions'])
    m3u.generate_all(romset.multi_images_softwares(), opts['m3u_dir'])


if __name__ == '__main__':
    _main(_parseargs())
