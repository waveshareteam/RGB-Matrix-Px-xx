#!/usr/bin/env python
import time

from PIL import Image

from samplebase import SampleBase
from samplepaths import default_example_image, expand_path


class ImageViewer(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageViewer, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default=default_example_image("runtext.ppm"))
        self.parser.add_argument("image_path", nargs="?", help="Optional positional image path for backward compatibility")

    def _get_image_path(self):
        image_path = self.args.image
        if image_path:
            return image_path
        if self.args.image_path:
            return self.args.image_path
        raise SystemExit("Require an image argument. Use -i/--image <file>.")

    def run(self):
        image = Image.open(expand_path(self._get_image_path()))
        image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
        self.matrix.SetImage(image.convert("RGB"))

        while True:
            time.sleep(100)


if __name__ == "__main__":
    image_viewer = ImageViewer()
    if (not image_viewer.process()):
        image_viewer.print_help()
