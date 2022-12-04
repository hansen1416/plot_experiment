from io import BytesIO
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image
# import pyproj

from main import muidsgrid, get_flooding_waterlevel_cmap


def data_heatmap(muids, data):

    muids = np.array(muids, dtype=int)

    grids = np.zeros((max(muids[:, 0])+1, max(muids[:, 1])+1))

    grids[muids[:, 0], muids[:, 1]] = 1

    return grids


def plot_heatmap(data):

    plt.imshow(data,
               # cmap=get_flooding_waterlevel_cmap(),
               interpolation='nearest')

    plt.gca().invert_yaxis()

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

    img.save(os.path.join('heatmaps', "heatmap.png"), format='PNG')


if __name__ == "__main__":

    muids = np.load(os.path.join('tmp', 'muids_3857.npy'))
    data = np.load(os.path.join('tmp', '1666857600.npy'))

    muids1 = muidsgrid(muids)

    plot_heatmap(data_heatmap(muids1, data))
