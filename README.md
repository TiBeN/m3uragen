m3uragen
========

m3uragen generates M3U files of multi images softwares from romsets
directories. Generated M3U files are intended to be used with RetroArch.

Overview
--------

The RetroArch emulators frontend supports multi images software (discs,
floppies etc.) using [M3U playlist
files](http://docs.retroachievements.org/Multi-Disc-Games-Tutorial/).  M3U
files have to created manually, which can be a tedious and boring task with big
images romsets (TOSEC, no-intro etc.). This tool scans your romset dirs and
create theses files automatically into a dir of your choice. 

It supports two kinds of romsets:

-   Zipped romsets

    In theses sets, each software has its own zip archive containing the images
    of the software. Because M3U files must contains path to unzipped images,
    m3uragen processes theses romsets in two steps: first it unzip the archives
    into a dir of your choice, then it creates M3U files with paths pointing 
    to the images from this dir.

-   Unzipped romsets

    In theses sets, images files are stored as is in the directory (or into
    subdirectories). m3uragen processes theses collections by scanning the 
    dir (optionnally recursivelly) and gathering image sets of the same software
    then creates a M3U file for each sets having more than one image. In order to proceed, 
    m3uragen must be provided a [regular expression](https://en.wikipedia.org/wiki/Regular_expression) 
    which determines the "media flag" part into the image file name. 
    Common rom collections (TOSEC, no-intro) 
    use [standard naming schemes](https://www.tosecdev.org/tosec-naming-convention) to
    name the images files, which contain among other thing "media flags" for multi images
    softwares. For example TOSEC use something like 'Some Game **(Disk 1 of 2)**.img'.

Installation
------------

### Using pip

To come...

### From the repo

Clone this repository, 'cd' into then launch using:

    $ ./bin/m3uragen <args>

Usage
-----

    $ m3uragen [-h] [-v] [-d] [-r] [-s SUFFIX] (-m MEDIA_FLAG_PATTERN | -z UNZIP_IMAGES) [-e IMAGE_EXTENSIONS] romset_dir m3u_dir

    positional arguments:
      romset_dir            Romset directory
      m3u_dir               M3U output directory

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      -d, --dry-run         execute in dry mode (don't write anything)
      -r, --recursive       scan romset dir recursivelly
      -s SUFFIX, --suffix SUFFIX
                            Add a suffix to M3U file names
      -m MEDIA_FLAG_PATTERN, --media-flag-pattern MEDIA_FLAG_PATTERN
                            regex used to extract media flags from image file name
      -z UNZIP_IMAGES, --unzip-images UNZIP_IMAGES
                            output directory where archives are unzipped
      -e IMAGE_EXTENSIONS, --image-extensions IMAGE_EXTENSIONS
                            filter images by extension (available only with -m)

Examples
--------

### Handle a zipped collection

Suppose you have a romset of zipped C64 floppy games.

The romset is organised like this into the dir '/c64-set'

    $ ls /c64-set

    [..]
    'Zeppelin Rescue (USA, Europe) (v1.3).zip'
    'Zeppelin (USA, Europe).zip'
    'Zig Zag (USA, Europe).zip'
    'Zoids (USA, Europe).zip'
    'Zone Ranger (USA, Europe).zip'
    'Zoom! (USA).zip'
    'Zork II - The Wizard of Frobozz (USA, Europe) (R22).zip'
    'Zork I - The Great Underground Empire (USA, Europe) (R52) (C128).zip'
    'Zorro (USA, Europe).zip'
    'Z-Pilot (Europe).zip'
    'Z-Pilot (USA).zip'
    'Zyron (Europe).zip'
    [..]

Because the images are zipped into archives, theses archives have to be unzipped before.
We want unzipped images to go to '/c64-dsk' and generated m3u files to '/c64-m3u'.
This is done by executing:

    $ m3uragen -v /c64-set /c64-m3u -z /c64-m3u

M3U files are named after the name of the zip archives:

    $ ls /c64-m3u

    [..]
    'World'\''s Greatest Football Game (USA, Europe).m3u'
    'World Tour Golf (USA, Europe).m3u'
    'WWF WrestleMania (Europe).m3u'
    'X-Men - Madness in Murderworld (USA, Europe) (Alt 1).m3u'
    'X-Men - Madness in Murderworld (USA, Europe).m3u'
    'X-Out (Europe) (Alt 1).m3u'
    'X-Out (Europe).m3u'
    'Zak McKracken and the Alien Mindbenders (Germany).m3u'
    'Zork I - The Great Underground Empire (USA, Europe) (R52) (C128).m3u'
    [..]

Paths to the images files into m3u are relatives to the M3U file.

### Handle an unzipped collection

Suppose you have some Atari ST floppies images named after the TOSEC naming conventions:

    $ ls /st-flop

    [..]
    Battleships (1987)(Elite)[!].stx
    Berlin 1948 (1989)(Time Warp)(Disk 1 of 2).stx
    Berlin 1948 (1989)(Time Warp)(Disk 2 of 2).stx
    Bermuda Project (1987)(Mirrorsoft)(Disk 1 of 2).stx
    Bermuda Project (1987)(Mirrorsoft)(Disk 2 of 2).stx
    Better Dead Than Alien! (1987)(Electra).stx
    Beverly Hills Cop (1990)(Paramount Pictures)(Disk 1 of 2).stx
    Beverly Hills Cop (1990)(Paramount Pictures)(Disk 2 of 2).stx
    [..]

For multi-images software, the image files names contain a media flag that follows
this pattern: '(Disk n of n)'. This pattern can be expressed with the following
regular expression: `\(Disk \d+ of \d+\)`.
M3U files of this collection can be generated into '/st-m3u' using:

    $ m3uragen -v /st-flop /st-m3u -m '\(Disk \d+ of \d+\)'

M3U files are named after the images filenames minus the media flag part:

    $ ls /st-m3u

    [..]
    Berlin 1948 (1989)(Time Warp).m3u
    Bermuda Project (1987)(Mirrorsoft).m3u
    Beverly Hills Cop (1990)(Paramount Pictures).m3u
    [..]

The regular expression can be tested again the romset without writing anything by 
combining verbose mode and dry run mode:

    $ m3uragen -v -d /st-flop /st-m3u -m '\(Disk \d+ of \d+\)'

This will output M3U files that would be generated without really create them.

If the romset directory is organised into subdirs e.g.:

    ├── Berlin 1948 (1989)(Time Warp)(Disk 1 of 2)
    │   └── Berlin 1948 (1989)(Time Warp)(Disk 1 of 2).stx
    ├── Berlin 1948 (1989)(Time Warp)(Disk 2 of 2)
    │   └── Berlin 1948 (1989)(Time Warp)(Disk 2 of 2).stx
    ├── Bermuda Project (1987)(Mirrorsoft)(Disk 1 of 2)
    │   └── Bermuda Project (1987)(Mirrorsoft)(Disk 1 of 2).stx
    ├── Bermuda Project (1987)(Mirrorsoft)(Disk 2 of 2)
    │   └── Bermuda Project (1987)(Mirrorsoft)(Disk 2 of 2).stx
    ├── Better Dead Than Alien! (1987)(Electra)
    │   └── Better Dead Than Alien! (1987)(Electra).stx
    ├── Beverly Hills Cop (1990)(Paramount)(Disk 1 of 2)
    │   └── Beverly Hills Cop (1990)(Paramount)(Disk 1 of 2).stx
    ├── Beverly Hills Cop (1990)(Paramount)(Disk 2 of 2)
    │   └── Beverly Hills Cop (1990)(Paramount)(Disk 2 of 2).stx

Simply tell m3uragen to scan dir recursivelly using '-r':

    $ m3uragen -v -r /st-flop /st-m3u -m '\(Disk \d+ of \d+\)'

### A more complex example: gamebasecpc romset

This Amstrad CPC romset is more challenging as it mixes many images formats
(cdt and dsk), presents a more complex media flag scheme and is organized into
subdirs:

    
    ├── A
    │   ├── Academy - Tau Ceti II (E) - Side A.cdt
    │   ├── Academy - Tau Ceti II (E) - Side A - EACH SIDE A IS DUPLICATED ON SIDE B.cdt
    │   ├── Academy - Tau Ceti II (E) - Side B.cdt
    │   ├── Academy - Tau Ceti II (E) - Side B - EACH SIDE A IS DUPLICATED ON SIDE B.cdt
    │   ├── Academy - Tau Ceti II (F).dsk
        [..]
    │   ├── Aventuriers (F), Les - Disk 1A.cdt
    │   ├── Aventuriers (F), Les - Disk 1A.dsk
    │   ├── Aventuriers (F), Les - Disk 1B.cdt
    │   ├── Aventuriers (F), Les - Disk 1B.dsk
    │   ├── Aventuriers (F), Les - Disk 2A.cdt
    │   ├── Aventuriers (F), Les - Disk 2A.dsk
    │   ├── Aventuriers (F), Les - Disk 2B.cdt
    │   ├── Aventuriers (F), Les - Disk 2B.dsk
    │   ├── Aventuriers (F), Les - Side 1A.cdt
    │   ├── Aventuriers (F), Les - Side 1B.cdt
    │   ├── Aventuriers (F), Les - Side 2A.cdt
    │   ├── Aventuriers (F), Les - Side 2B.cdt
        [..]
    ├── B
    │   ├── Baba's Palace (E).cdt
    │   ├── Baba's Palace (E).dsk
    │   ├── Baby Jo (E) - Disk 1A.dsk
    │   ├── Baby Jo (E) - Disk 1B.dsk
    │   ├── Backgammon (E).cdt
        [..]

Generating M3U for this collection can be handled in two passes, one per image format.
The media flag pattern is the following: ` - (Disk|Side) [A-Z0-9]+[^.]*`.
Each pass is filtered by file extension using `-i <extension>`. In order to prevent clash
in M3U filenames between formats, a flag containing the image format will be added at 
the end of the M3U filename, using `-s <suffix>`: 

    $ m3uragen -v /romset /romset-m3u -m ' - (Disk|Side) [A-Z0-9]+[^.]*' -r -s ' (cdt)' -e cdt
    $ m3uragen -v /romset /romset-m3u -m ' - (Disk|Side) [A-Z0-9]+[^.]*' -r -s ' (dsk)' -e dsk
    
    $ ls /romset-m3u

    [..]
    Academy - Tau Ceti II (E) (cdt).m3u
    Aventuriers (F), Les (cdt).m3u
    Aventuriers (F), Les (dsk).m3u
    Baby Jo (E) (dsk).m3u
    [..]
 
