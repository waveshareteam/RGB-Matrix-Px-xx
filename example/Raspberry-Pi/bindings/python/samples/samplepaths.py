#!/usr/bin/env python
import os


SAMPLES_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SAMPLES_DIR, "../../.."))
MEDIA_DIR = os.path.abspath(os.path.join(SAMPLES_DIR, "../media"))


def project_path(*parts):
    return os.path.join(PROJECT_ROOT, *parts)


def media_path(*parts):
    return os.path.join(MEDIA_DIR, *parts)


def sample_path(*parts):
    return os.path.join(SAMPLES_DIR, *parts)


def default_font(font_name):
    return project_path("fonts", font_name)


def default_example_image(image_name):
    return project_path("examples-api-use", image_name)


def expand_path(path_value):
    return os.path.abspath(os.path.expanduser(path_value))
