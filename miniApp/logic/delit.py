import os
import glob
import eel


def dellAll():
    files = glob.glob('../web/sourse/*.png')

    for f in files:
        os.remove(f)

