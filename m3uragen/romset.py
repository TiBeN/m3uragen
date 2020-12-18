"""
RomSet classes
"""

import zipfile
import os
import re
from software import Software
from image import Image


class RomSet:
    """
    RomSet abstract base class
    """

    def __init__(self, dir, scan_subdirs):
        self._dir = dir
        self._scan_subdirs = scan_subdirs

    def multi_images_softwares(self):
        """
        Return softwares having more than one image file.
        To be implemented on children classes
        """
        return


class ZipRomSet(RomSet):

    def __init__(self, dir, scan_subdirs):
        self._multi_images_softwares = []
        super().__init__(dir, scan_subdirs)

    def multi_images_softwares(self):
        """
        Return software having more than one image file.
        These are detected during unzip operation
        """
        return self._multi_images_softwares

    def unzip_images_to(self, out_dir):
        """
        Unzip software images from zip files
        and store multi images softwares internally
        """
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
        archive.extractall(out_dir)
        members = archive.infolist()
        if len(members) > 1:
            software = Software(path.with_suffix('').name)
            for i in members:
                software.add_image(Image(os.path.join(out_dir, i.filename)))
                self._multi_images_softwares.append(software)


class NonZipRomSet(RomSet):

    def __init__(self, dir, scan_subdirs, media_flag_pattern, image_extensions):
        self._media_flag_re = re.compile('.*(' + media_flag_pattern + ').*')
        self._image_extensions = image_extensions
        super().__init__(dir, scan_subdirs)

    def multi_images_softwares(self): 
        """
        Scan files on the romset dir, combine software files using the
        media flag pattern then return softwares having more than one 
        image file
        """
        return self._scan_dirs(self._dir).values()

    def _scan_dirs(self, dir, softwares=dict()):
        # self.multi_image_softwares() helper that handle
        # directories scanning
        for path in dir.iterdir():
            
            if path.is_dir() and self._scan_subdirs:
                self._scan_dirs(path, softwares)
                continue
            
            if not self._suffix_match(path):
                continue
            
            image = Image(path)
            media_flag = image.extract_media_flag(self._media_flag_re)

            if not media_flag:
                continue
            
            software_name = image.path.with_suffix('').name.replace(media_flag, '')
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
