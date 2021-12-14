import os
import sys

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

SCALE = 96

SCREEN_HEIGHT = 768
SCREEN_WIDTH = 960

if getattr(sys, "frozen", False):
    DIR_PATH = os.path.dirname(sys.executable)
elif __file__:
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
