"""Software class"""


class Software:

    def __init__(self, name):
        self.name = name
        self._images = []

    def add_image(self, image):
        self._images.append(image)

    def images(self):
        return sorted(self._images, key=lambda i: i.path)

    def nb_images(self):
        return len(self._images)

    def move_images_to(self, out_dir):
        for i in self._images:
            i.move_to(out_dir)

