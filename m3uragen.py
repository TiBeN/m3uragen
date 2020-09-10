#!/usr/bin/env python3

from pathlib import Path
import sys

# Process arguments

if len(sys.argv) < 3:
    sys.stderr('ERROR: bad number of arguments')
    sys.exit(-1)

colpath = Path(sys.argv[1]).resolve()
m3upath = Path(sys.argv[2]).resolve()
patterns = sys.argv[3:]


