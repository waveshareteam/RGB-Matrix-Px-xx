#!/usr/bin/env python
from PIL import Image

from samplebase import SampleBase


class GifViewer(SampleBase):
    def __init__(self, *args, **kwargs):
        super(GifViewer, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The GIF image to display", default=None)
        self.parser.add_argument(
            "--framerate-fraction",
            help="Fractional playback divisor passed to SwapOnVSync(). Default: 10",
            default=10,
            type=int,
        )
        self.parser.add_argument("image_path", nargs="?", help="Optional positional GIF path for backward compatibility")

    def _get_image_path(self):
        image_path = self.args.image
        if image_path:
            return image_path
        if self.args.image_path:
            return self.args.image_path
        raise SystemExit("Require a gif argument. Use -i/--image <file.gif>.")

    def _load_frames(self, image_path):
        gif = Image.open(image_path)

        try:
            num_frames = gif.n_frames
        except Exception:
            gif.close()
            raise SystemExit("provided image is not a gif")

        frames = []
        frame_index = 0
        while frame_index < num_frames:
            gif.seek(frame_index)
            frame = gif.copy()
            frame.thumbnail((self.matrix.width, self.matrix.height), Image.LANCZOS)
            frames.append(frame.convert("RGB"))
            frame_index += 1

        gif.close()
        return frames

    def run(self):
        if self.args.framerate_fraction < 1:
            raise SystemExit("--framerate-fraction must be >= 1")

        image_path = self._get_image_path()
        canvas = self.matrix.CreateFrameCanvas()

        print("Preprocessing gif, this may take a moment depending on the size of the gif...")
        frames = self._load_frames(image_path)
        print("Completed preprocessing, displaying gif")

        frame_count = len(frames)
        cur_frame = 0
        while True:
            canvas.SetImage(frames[cur_frame])
            canvas = self.matrix.SwapOnVSync(
                canvas,
                framerate_fraction=self.args.framerate_fraction,
            )
            cur_frame = (cur_frame + 1) % frame_count


if __name__ == "__main__":
    gif_viewer = GifViewer()
    if (not gif_viewer.process()):
        gif_viewer.print_help()
