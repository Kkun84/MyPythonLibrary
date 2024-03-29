
import platform

import cv2
import skvideo.io
import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import PIL


def show_images(images, title=None, *, cols=1, rows=1, size=[1, 1], verbose=0):
    # 複数画像表示関数
    figsize = [x * y for x, y in zip(size, [cols, rows])]
    fig = plt.figure(figsize=figsize)
    for i, im in enumerate(images):
        if i + 1 > cols * rows:
            break
        if verbose == 1:
            print(f"\r{i:{len(str(cols*rows))}}/{cols*rows}", end='')
        ax = fig.add_subplot(rows, cols, i+1)
        if im.ndim == 2:
            ax.imshow(im, 'gray')
        else:
            ax.imshow(im)
            if title is not None:
                ax.set_title(title)
        ax.axis('off')
    print(end='\r')
    plt.show()
    return


def lower_quality(src, size):
    dst = PIL.Image.fromarray(src)
    dst.thumbnail(size)
    dst = np.array(dst)
    return dst


def make_animation(array, fps=50, figsize=None, path=None):
    fig = plt.figure(figsize=None)
    # plt.axis('off')
    ims = [[plt.imshow(im)] for im in array]
    ani = animation.ArtistAnimation(fig, ims, interval=1000/fps)
    if path is not None:
        ani.save(path, writer="ffmpeg")
    plt.close(fig)
    return ani


def save_as_mp4(path, array, fps=50):
    if platform.linux_distribution()[0]:
        # Linux
        skvideo.io.vwrite(path, array, inputdict={'-r': str(fps)})
    else:
        # other OS
        dim = array[0].ndim
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(path, fourcc, fps,
                              array[0].shape[1::-1], isColor=dim == 3)
        for im in array:
            if im.dtype.kind == 'b':
                im = im.astype(np.uint8) * 0xff
            elif im.dtype.kind == 'f':
                im = (im * 0xff).astype(np.uint8)
            else:
                im = im.astype(np.uint8)
            if dim == 3:
                im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
            out.write(im)
        out.release()
