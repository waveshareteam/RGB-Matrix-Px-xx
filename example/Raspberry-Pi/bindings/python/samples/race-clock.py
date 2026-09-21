#!/usr/bin/env python
import datetime
import subprocess
import time

from rgbmatrix import graphics

from samplebase import SampleBase
from samplepaths import default_font, expand_path


class RaceClock(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RaceClock, self).__init__(*args, **kwargs)
        self.parser.set_defaults(
            led_rows=32,
            led_cols=64,
            led_gpio_mapping="adafruit-hat",
            led_slowdown_gpio=3,
            led_pwm_bits=1,
            drop_privileges=False,
        )
        self.parser.add_argument("--font-clock", help="Optional font used for the clock text", default="")
        self.parser.add_argument("--font-countdown", help="Optional font used for the countdown text", default="")
        self.parser.add_argument("--font-start", help="Optional font used for the start message", default="")
        self.parser.add_argument("--countdown-length", help="Countdown cycle length in seconds", default=10, type=int)
        self.parser.add_argument("--countdown-prefix", help="Prefix displayed before the countdown value", default="T-")
        self.parser.add_argument("--start-text", help="Message shown when countdown reaches one", default="START")
        self.parser.add_argument("--sound", help="Optional WAV file played when countdown reaches four", default="")

        self._sound_played = False

    def _load_font(self, font_path):
        font = graphics.Font()
        font.LoadFont(expand_path(font_path))
        return font

    def _text_width(self, font, text):
        width = 0
        for char in text:
            width += font.CharacterWidth(ord(char))
        return width

    def _fit_font(self, candidates, sample_text, max_width, max_height):
        for font_path in candidates:
            font = self._load_font(font_path)
            if font.height > max_height:
                continue
            if self._text_width(font, sample_text) > max_width:
                continue
            return font
        return self._load_font(candidates[-1])

    def _choose_font(self, requested_font, sample_text, band_width, band_height, candidates):
        if requested_font:
            return self._load_font(requested_font)
        return self._fit_font(candidates, sample_text, band_width, band_height)

    def _draw_centered_text(self, font, baseline_y, color, text):
        text_width = self._text_width(font, text)
        x_pos = max(0, (self.matrix.width - text_width) // 2)
        graphics.DrawText(self.matrix, font, x_pos, baseline_y, color, text)

    def _band_baseline(self, top_y, bottom_y, font):
        band_height = max(1, bottom_y - top_y)
        text_height = max(1, font.height)
        return top_y + max(font.baseline, (band_height + text_height) // 2 - 1)

    def _layout_fonts(self):
        font_candidates = [
            default_font("9x18B.bdf"),
            default_font("8x13B.bdf"),
            default_font("7x13B.bdf"),
            default_font("7x13.bdf"),
            default_font("6x10.bdf"),
            default_font("5x7.bdf"),
            default_font("4x6.bdf"),
            default_font("tom-thumb.bdf"),
        ]
        clock_band_height = max(8, self.matrix.height * 2 // 5)
        countdown_band_height = max(8, self.matrix.height - clock_band_height)
        start_band_height = max(8, self.matrix.height - 2)

        clock_font = self._choose_font(
            self.args.font_clock,
            "88:88:88",
            self.matrix.width - 2,
            clock_band_height - 2,
            font_candidates,
        )
        countdown_font = self._choose_font(
            self.args.font_countdown,
            f"{self.args.countdown_prefix}{self.args.countdown_length:02d}",
            self.matrix.width - 2,
            countdown_band_height - 2,
            font_candidates,
        )
        start_font = self._choose_font(
            self.args.font_start,
            self.args.start_text,
            self.matrix.width - 2,
            start_band_height - 2,
            font_candidates,
        )
        return clock_font, countdown_font, start_font

    def _play_audio(self):
        if not self.args.sound:
            return
        subprocess.Popen(["aplay", expand_path(self.args.sound)])

    def _show_start(self, start_font):
        green = graphics.Color(0, 255, 0)
        self.matrix.Clear()
        baseline_y = self._band_baseline(0, self.matrix.height, start_font)
        self._draw_centered_text(start_font, baseline_y, green, self.args.start_text)
        time.sleep(1)

    def _draw_clock(self, clock_font, countdown_font, start_font, clock_text, countdown):
        red = graphics.Color(255, 0, 0)
        white = graphics.Color(255, 255, 255)
        split_y = max(1, self.matrix.height * 2 // 5)
        clock_baseline = self._band_baseline(0, split_y, clock_font)
        countdown_baseline = self._band_baseline(split_y, self.matrix.height, countdown_font)
        countdown_text = f"{self.args.countdown_prefix}{countdown:02d}"

        self.matrix.Clear()
        self._draw_centered_text(clock_font, clock_baseline, red, clock_text)

        if countdown > 5:
            self._sound_played = False
            self._draw_centered_text(countdown_font, countdown_baseline, white, countdown_text)
            return

        self._draw_centered_text(countdown_font, countdown_baseline, red, countdown_text)
        if countdown == 4 and not self._sound_played:
            self._play_audio()
            self._sound_played = True
        if countdown != 1:
            return

        time.sleep(1)
        self._show_start(start_font)

    def run(self):
        if self.args.countdown_length < 1:
            raise SystemExit("--countdown-length must be >= 1")

        clock_font, countdown_font, start_font = self._layout_fonts()

        while True:
            start_time = datetime.datetime.now()
            clock_text = start_time.strftime("%H:%M:%S")
            countdown = abs((int(start_time.second) % self.args.countdown_length) - self.args.countdown_length)

            self._draw_clock(clock_font, countdown_font, start_font, clock_text, countdown)

            elapsed_time = (datetime.datetime.now() - start_time).total_seconds()
            time.sleep(max(0, 1 - elapsed_time))


if __name__ == "__main__":
    race_clock = RaceClock()
    if (not race_clock.process()):
        race_clock.print_help()
