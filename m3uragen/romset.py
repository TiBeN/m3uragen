"""RomSet classes"""

from pathlib import Path
import zipfile
import os
import re
import logging
from m3uragen.software import Software
from m3uragen.image import Image


class RomSet:
    """RomSet abstract base class"""

    def __init__(self, dir, scan_subdirs, dry_run):
        self._dir = dir
        self._scan_subdirs = scan_subdirs
        self._dry_run = dry_run

    def get_softwares(self):
        """Return softwares.
        To be implemented on children classes
        """
        return


class ZipRomSet(RomSet):

    def __init__(self, dir, scan_subdirs, dry_run):
        self._softwares = []
        super().__init__(dir, scan_subdirs, dry_run)

    def get_softwares(self):
        """Return software having more than one image file.
        These are detected during unzip operation
        """
        return sorted(self._softwares, key=lambda i: i.name)

    def unzip_images_to(self, out_dir):
        """Unzip software images from zip files
        and store multi images softwares internally
        """
        if not self._dry_run:
            if not out_dir.exists():
                out_dir.mkdir(parents=True)
        self._scan_dir(self._dir, out_dir)
        
    def _scan_dir(self, dir, out_dir):
        # self.unzip_images_to() helper that handle
        # directories scanning
        for path in dir.iterdir():
            if path.is_dir() and self._scan_subdirs:
                self._scan_dir(path, out_dir)
            if zipfile.is_zipfile(path):
                self._process_archive(path, out_dir)

    def _process_archive(self, path, out_dir):
        # self._scan_dir() helper that unzip image
        # files then fill the multi_image_software list
        archive = zipfile.ZipFile(path)
        if not self._dry_run:
            archive.extractall(out_dir)
        logging.info('Unzipped %s', path.name)
        software = Software(path.with_suffix('').name)
        for i in archive.infolist():
            software.add_image(Image(Path(os.path.join(out_dir, i.filename))))
        self._softwares.append(software)


class NonZipRomSet(RomSet):

    def __init__(self, dir, scan_subdirs, media_flag_pattern, filter_patterns, 
                 image_extensions, dry_run):
        self._media_flag_re = re.compile('.*?(' + media_flag_pattern + ').*')
        self._image_extensions = image_extensions
        self._filter_res = []
        if filter_patterns: 
            for i in filter_patterns:
                self._filter_res.append(re.compile(i))

        super().__init__(dir, scan_subdirs, dry_run)

    def get_softwares(self): 
        """Scan files on the romset dir, combine software files using the
        media flag pattern then return softwares
        """
        softwares = self._scan_dirs(self._dir).values()
        return sorted(softwares, key=lambda i: i.name)

    def _scan_dirs(self, dir, softwares=dict()):
        # self.multi_image_softwares() helper that handle
        # directories scanning
        for path in dir.iterdir():
            
            if path.is_dir() and self._scan_subdirs:
                self._scan_dirs(path, softwares)
                continue
            
            if not self._suffix_match(path):
                continue

            if self._filter_match(path.name):
                continue

            image = Image(path)
            media_flag = image.extract_media_flag(self._media_flag_re)

            software_name = image.path.with_suffix('').name
            if media_flag:
                software_name = software_name.replace(media_flag, '')
            
            if software_name not in softwares:
                softwares[software_name] = Software(software_name)
            softwares[software_name].add_image(image)

        return softwares

    def _suffix_match(self, path):
        if not self._image_extensions:
            return True
        for i in self._image_extensions:
            if '.' + i == path.suffix:
                return True

    def _filter_match(self, name):
        for i in self._filter_res:
            if i.search(name):
                return True
        return False            

