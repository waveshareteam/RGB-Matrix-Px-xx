#!/usr/bin/env python
from rgbmatrix import graphics

from samplebase import SampleBase
from samplepaths import default_font, expand_path


class HelloLayout(SampleBase):
    def __init__(self, *args, **kwargs):
        super(HelloLayout, self).__init__(*args, **kwargs)
        self.parser.add_argument("--line1", help="First line text", default="Hello Pi5")
        self.parser.add_argument("--line2", help="Second line text", default="Welcome")
        self.parser.add_argument("--line3", help="Third line text", default="RGB Matrix")
        self.parser.add_argument(
            "--size-format",
            help="Last line template. Available fields: {width}, {height}",
            default="{width}x{height}",
        )
        self.parser.add_argument("--font", help="Optional BDF font path", default="")

    def _load_font(self, font_path):
        font = graphics.Font()
        font.LoadFont(expand_path(font_path))
        return font

    def _text_width(self, font, text):
        width = 0
        for char in text:
            width += font.CharacterWidth(ord(char))
        return width

    def _pick_font(self, lines):
        if self.args.font:
            return self._load_font(self.args.font)
        return self._load_font(default_font("6x10.bdf"))

    def _line_gap(self, font):
        base_gap = max(1, font.height // 3)
        gap_overrides = {
            (80, 40): 1,
            (64, 32): 1,
        }
        return gap_overrides.get((self.matrix.width, self.matrix.height), base_gap)

    def _special_layout(self, font, lines):
        baselines_by_size = {
            (80, 40): [8, 18, 29, 38],
            (64, 32): [7, 15, 23, 31],
        }
        baselines = baselines_by_size.get((self.matrix.width, self.matrix.height))
        if baselines is None:
            return None

        positions = []
        index = 0
        while index < len(lines):
            line = lines[index]
            text_width = self._text_width(font, line)
            x_pos = max(0, (self.matrix.width - text_width) // 2)
            positions.append((line, x_pos, baselines[index]))
            index += 1
        return positions

    def _layout_lines(self, font, lines):
        special_positions = self._special_layout(font, lines)
        if special_positions is not None:
            return special_positions

        gap = self._line_gap(font)
        block_height = font.height * len(lines) + gap * (len(lines) - 1)
        top_y = max(0, (self.matrix.height - block_height) // 2)

        positions = []
        index = 0
        while index < len(lines):
            line = lines[index]
            text_width = self._text_width(font, line)
            x_pos = max(0, (self.matrix.width - text_width) // 2)
            baseline_y = top_y + font.baseline + index * (font.height + gap)
            positions.append((line, x_pos, baseline_y))
            index += 1
        return positions

    def _line_gradients(self):
        return [
            ((255, 80, 80), (255, 220, 80)),
            ((80, 255, 120), (80, 220, 255)),
            ((80, 160, 255), (180, 80, 255)),
            ((255, 120, 220), (120, 255, 220)),
        ]

    def _interpolate_color(self, start_rgb, end_rgb, numerator, denominator):
        if denominator <= 0:
            return graphics.Color(start_rgb[0], start_rgb[1], start_rgb[2])

        red = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * numerator // denominator
        green = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * numerator // denominator
        blue = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * numerator // denominator
        return graphics.Color(red, green, blue)

    def _draw_gradient_text(self, font, x_pos, baseline_y, text, start_rgb, end_rgb):
        if not text:
            return

        denominator = max(1, len(text) - 1)
        cursor_x = x_pos
        index = 0
        while index < len(text):
            char = text[index]
            color = self._interpolate_color(start_rgb, end_rgb, index, denominator)
            cursor_x += font.DrawGlyph(self.matrix, cursor_x, baseline_y, color, ord(char))
            index += 1

    def run(self):
        size_text = self.args.size_format.format(width=self.matrix.width, height=self.matrix.height)
        lines = [
            self.args.line1,
            self.args.line2,
            self.args.line3,
            size_text,
        ]

        font = self._pick_font(lines)
        positions = self._layout_lines(font, lines)
        line_gradients = self._line_gradients()

        while True:
            self.matrix.Clear()
            index = 0
            while index < len(positions):
                line, x_pos, baseline_y = positions[index]
                start_rgb, end_rgb = line_gradients[index]
                self._draw_gradient_text(font, x_pos, baseline_y, line, start_rgb, end_rgb)
                index += 1
            self.usleep(100000)


if __name__ == "__main__":
    hello_layout = HelloLayout()
    if (not hello_layout.process()):
        hello_layout.print_help()
