"""m3uragen main entry point"""

from pathlib import Path
from m3uragen.romset import ZipRomSet, NonZipRomSet
from m3uragen import m3u
import logging
import sys
import argparse
import re


def _parseargs():

    parser = argparse.ArgumentParser(
            description="Generate M3U files of multi-images software romsets")
    
    parser.add_argument('romset_dir', help='Romset directory')
    parser.add_argument('m3u_dir', help='M3U output directory')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', 
                        action='store_true')
    parser.add_argument('-d', '--dry-run', 
                        help='execute in dry mode (don\'t write anything)', 
                        action='store_true')
    parser.add_argument('-r', '--recursive', 
                        help='scan romset dir recursivelly', 
                        action='store_true')

    parser.add_argument('-s', '--suffix', 
                        help='Add a suffix to M3U file names')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-m', '--media-flag-pattern', 
                       help='regex used to extract media flags from image file name')
    group.add_argument('-z', '--unzip-images', 
                       help='output directory where archives are unzipped')

    parser.add_argument('-e', '--image-extensions', 
                        help='filter images by extension (available only with -m)', 
                        action='append')
    args = parser.parse_args()

    if not Path(args.romset_dir).resolve().is_dir():
        logging.error('%s is not a valid directory', args.romset_dir)
        sys.exit(1)

    if args.media_flag_pattern:
        try:
            re.compile(args.media_flag_pattern)
        except re.error:
            logging.error('\'%s\' is not a valid regular expression', 
                          args.media_flag_pattern)
            sys.exit(1)

    args.romset_dir = Path(args.romset_dir)
    args.m3u_dir = Path(args.m3u_dir)
    if (args.unzip_images):
        args.unzip_images = Path(args.unzip_images)
    
    return args
    

def main():

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(lambda record: record.levelno <= logging.INFO)
    verb_handler = logging.StreamHandler(sys.stderr)
    verb_handler.setLevel(logging.WARNING)
    logging.basicConfig(format='%(levelname)s:%(message)s', 
                        handlers=[handler, verb_handler])

    args = _parseargs()

    logging.getLogger().setLevel(
            logging.INFO if args.verbose else logging.WARNING)

    if args.unzip_images:
        romset = ZipRomSet(args.romset_dir, args.recursive, args.dry_run)
        try: 
            romset.unzip_images_to(args.unzip_images)
        except PermissionError as err:
            logging.error('Can\'t create %s: permission denied', err.filename)
            sys.exit(1)
    else:
        romset = NonZipRomSet(args.romset_dir, args.recursive, 
                              args.media_flag_pattern, 
                              args.image_extensions, args.dry_run)

    try: 
        m3u.generate_all(romset.multi_images_softwares(), args.m3u_dir, 
                         args.suffix, args.dry_run)
    except PermissionError as err:
        logging.error('Can\'t create %s: permission denied', err.filename)
        sys.exit(1)


if __name__ == '__main__':
    main()
