import io
from urllib.request import urlopen

from PIL import Image

from samplebase import SampleBase
from samplepaths import expand_path, media_path

class StillViewer(SampleBase):
    def __init__(self, *args, **kwargs):
        super(StillViewer, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="Image Location or URL", default=media_path("catnaps.jpg"))

    def run(self):
        while True:
            image_source = self.args.image
            if image_source.find("http") >= 0:
                with urlopen(image_source) as fd:
                    image_file = io.BytesIO(fd.read())
                im = Image.open(image_file).convert('RGB')
            else:
                im = Image.open(expand_path(image_source)).convert('RGB')
            if im.size[0] > im.size[1]:
                size = (self.matrix.width + self.matrix.width, self.matrix.width)
                im.thumbnail(size)
            else:
                size = (self.matrix.height, self.matrix.height + self.matrix.height)
                im.thumbnail(size)
            width, height = im.size
            left = (width - self.matrix.width) // 2
            top = (height - self.matrix.height) // 2
            right = left + self.matrix.width
            bottom = top + self.matrix.height
            image = im.crop((int(left), int(top), int(right), int(bottom)))

            image.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
            self.matrix.SetImage(image)

# Main function
# e.g. call with
#  sudo ./still-viewer.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    still_viewer = StillViewer()
    if (not still_viewer.process()):
        still_viewer.print_help()

# Created By: Mr. CatNaps
# Date: 10/15/2019
# Description:
# StillViewer will automatically take a local or web image and display it on a LED Matrix. 
# StillViewer will also determine if the image is landscape or portrait and automatically resize and crop it.
# It has the latest option flags and supports U-mapping. 
# Set the '-i=' flag to a local path or a URL and it is ready to go.
