"""Software class"""


class Software:

    def __init__(self, name):
        self.name = name
        self._images = []

    def add_image(self, image):
        self._images.append(image)

    def images(self):
        return sorted(self._images, key=lambda i: i.path)
