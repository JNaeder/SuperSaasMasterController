import sys
import os


def create_path(original_image_path):
    bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    new_image_path = os.path.abspath(os.path.join(bundle_dir, original_image_path))
    return new_image_path
