from io import BytesIO
import os
from random import choices
from string import ascii_uppercase, digits

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from main import get_flooding_waterlevel_cmap


def random_string(k=6):

    population = ascii_uppercase + digits
    return str.join('', choices(population, k=k))


def random_data(width=72, height=72):

    np.random.seed(42)

    data = np.array(np.meshgrid(list(range(width)),
                    list(range(height)))).T.reshape(-1, 2)

    data = np.append(data, np.random.rand(
        width*height).T.reshape(-1, 1), axis=1)

    return data


def simple_scatter_plot(data, figsize=(1, 1), s=0.2):

    plt.figure(figsize=figsize)

    # plt.axis('off')
    plt.tight_layout()

    x = np.array(data[:, 0], dtype=int)
    y = np.array(data[:, 1], dtype=int)

    plt.scatter(x, y, c=data[:, 2],
                alpha=1, edgecolors='none', linewidths=0, marker='s',
                s=s,
                cmap=get_flooding_waterlevel_cmap(), vmin=0, vmax=1)

    img_buf = BytesIO()

    plt.savefig(img_buf, transparent=True, dpi=200,
                format='png')  # , pad_inches=0)

    plt.clf()
    plt.close()

    img_buf.seek(0)

    img = Image.open(img_buf)

    # Cropped image of above dimension
    # (It will not change original image)
    # img = img.crop(self.crop_box[img_size])

    alpha_channel = img.getchannel('A')

    # Make all opaque pixels into semi-opaque
    alpha_channel = alpha_channel.point(
        lambda i: 128 if i > 0 else 0)

    img.putalpha(alpha_channel)

    img.save(os.path.join('simpleplot', "simple_plot_{}_{}.png".format(
        str(figsize), str(s))), format='PNG')


if __name__ == "__main__":

    data = random_data()

    simple_scatter_plot(data, figsize=(1, 1), s=0.3)

    exit()

    # fig = list(range(1, 16))
    # s = [0.5, 2, 4.2, 8, 12, 18, 24, 32, 40, 50, 60, 72, 84, 96, 110]

    # for i, f in enumerate(fig):

    #     simple_scatter_plot(data, figsize=(f, f), s=s[i])
