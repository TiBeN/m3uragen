"""
Image class
"""


class Image:

    def __init__(self, path):
        self.path = path

    def extract_media_flag(self, media_flag_re):
        match = media_flag_re.match(self.path.name)
        if match:
            return match.group(1)
