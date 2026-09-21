#!/usr/bin/env python
import time
from PIL import Image
from samplebase import SampleBase
from samplepaths import default_example_image, expand_path


class ImageScroller(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageScroller, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default=default_example_image("runtext.ppm"))

    def run(self):
        if "image" not in self.__dict__:
            self.image = Image.open(expand_path(self.args.image)).convert("RGB")
            src_w, src_h = self.image.size
            scaled_w = max(1, int(src_w * self.matrix.height / src_h))
            self.image = self.image.resize((scaled_w, self.matrix.height), Image.LANCZOS)

        double_buffer = self.matrix.CreateFrameCanvas()
        img_width = self.image.size[0]

        xpos = 0
        while True:
            xpos += 1
            if xpos > img_width:
                xpos = 0

            double_buffer.Clear()
            double_buffer.SetImage(self.image, -xpos)
            double_buffer.SetImage(self.image, -xpos + img_width)
            double_buffer = self.matrix.SwapOnVSync(double_buffer)
            time.sleep(0.01)

# Main function
# e.g. call with
#  sudo ./image-scroller.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_scroller = ImageScroller()
    if (not image_scroller.process()):
        image_scroller.print_help()
