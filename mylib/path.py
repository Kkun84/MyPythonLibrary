import os
import numpy as np


def time_sort(files):
    time_rank = np.argsort([os.path.getmtime(file) for file in files])
    dst = list(np.array(files)[time_rank])
    return dst


def split(file):
    dirname, basename = os.path.split(file)
    root, ext = os.path.splitext(basename)
    return dirname, root, ext
