#!/usr/bin/env python
from PIL import Image
from PIL import ImageDraw
import time

from samplebase import SampleBase


class ImageDrawDemo(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageDrawDemo, self).__init__(*args, **kwargs)
        self.parser.add_argument("--step-delay", help="Delay between animation steps in seconds", default=0.05, type=float)

    def run(self):
        image = Image.new("RGB", (self.matrix.width, self.matrix.height))
        draw = ImageDraw.Draw(image)
        max_x = self.matrix.width - 1
        max_y = self.matrix.height - 1

        draw.rectangle((0, 0, max_x, max_y), fill=(0, 0, 0), outline=(0, 0, 255))
        draw.line((0, 0, max_x, max_y), fill=(255, 0, 0))
        draw.line((0, max_y, max_x, 0), fill=(0, 255, 0))

        offset = -self.matrix.width
        while offset <= self.matrix.width:
            self.matrix.Clear()
            self.matrix.SetImage(image, offset, offset)
            time.sleep(self.args.step_delay)
            offset += 1

        self.matrix.Clear()


if __name__ == "__main__":
    image_draw_demo = ImageDrawDemo()
    if (not image_draw_demo.process()):
        image_draw_demo.print_help()
