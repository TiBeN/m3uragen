"""Software image class"""

import os

class Image:

    def __init__(self, path):
        self.path = path

    def extract_media_flag(self, media_flag_re):
        match = media_flag_re.match(self.path.name)
        if match:
            return match.group(1)

    def move_to(self, out_dir):
        self.path = self.path.replace(os.path.join(out_dir, self.path.name))
