#!/usr/bin/env python3

import argparse
import sys


def main(args):

    # Process arguments
     
    parser = argparse.ArgumentParser(prog='m3uragen', 
                                     description='Generate M3U playlist files'
                                                 'from romsets for RetroArch')
    parser.add_argument('filenames', nargs='+')
    args = parser.parse_args()
    print(args)


if __name__ == '__main__':
    main(sys.argv)
