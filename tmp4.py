from io import BytesIO
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from PIL import Image
import pyproj


def get_flooding_waterlevel_cmap(vmin=0.0, vmax=2.8847, percentile25=0.0031, percentile50=0.0211, percentile75=0.1556):
    
    total = vmax - vmin

    v = [
        (0.0, '#5FB5C0'), # 0.0m
        ((percentile25 - vmin)/total, '#5FB5C0'),
        ((percentile50 - vmin)/total, '#35A66A'),
        ((percentile75 - vmin)/total, '#EBAA15'),
        ((percentile75 - vmin + total/10000)/total, '#e33353'),
        (1.0, '#e33353'), # 1.5m
    ]

    return colors.LinearSegmentedColormap.from_list(
        'flood_cmap', v)


def _generate_flood_png3857(muids, flood_data, image_file: str):
    """Generate flooding images

    read all flooding data from .npy
    combine with muids
    scatter a image, crop to the box that is in desired lat,lng range

    Args:
        cmap: custom color map
        muids: grid ids in coords 3857
        flood_data: flood water depth from DHI
        image_file: image oss key
        img_size: 0 | 1, 0 is a small sized image (1314x952), 1 is larger (3370x2091)

    """

    grid2D = {
        "j0": 1751622.5000000084,
        "k0": 5947162.5000000652,
        "numJ": 273,
        "numK": 189,
        "deltaJ": 5.0,
        "deltaK": 5.0
    }

    crs_dhi = 'PROJCS[\"NZGD2000 / New Zealand Transverse Mercator 2000\",GEOGCS[\"NZGD2000\",DATUM[\"New_Zealand_Geodetic_Datum_2000\",'+\
    'SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6167\"]],'+\
    'PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],' +\
    'AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],AUTHORITY[\"EPSG\",\"4167\"]],PROJECTION[\"Transverse_Mercator\"],' +\
    'PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",173],PARAMETER[\"scale_factor\",0.9996],' +\
    'PARAMETER[\"false_easting\",1600000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],' +\
    'AUTHORITY[\"EPSG\",\"2193\"]]'
    transformer_dhi3857 = pyproj.Transformer.from_crs(crs_dhi, pyproj.CRS.from_epsg(3857))

    flooding_masked = flood_data
    muids_masked = muids

    flooding_masked = flood_data
    muids_masked = muids

    x3857, y3857 = transformer_dhi3857.transform(np.array([grid2D['j0'], grid2D['j0']+grid2D['numJ']*grid2D['deltaJ']]), \
                                        np.array([grid2D['k0'], grid2D['k0']+grid2D['numK']*grid2D['deltaK']]))
    # this is the rectangle location to place the image on bing map
    rectangle3857 = {'x_0': x3857[0], 'x_n': x3857[1], 'y_0': y3857[0], 'y_n': y3857[1]}
    # figure size needs to be proportionate to the coordinates
    figsize = (grid2D['numJ']/10, grid2D['numK']/10)

    plt.figure(figsize=figsize)

    plt.axis('off')
    plt.tight_layout()

    # plt.xlim([rectangle3857['x_0'], rectangle3857['x_n']])
    # plt.ylim([rectangle3857['y_0'], rectangle3857['y_n']])

    plt.scatter(muids_masked[:, 0], muids_masked[:, 1], s=20, c=flooding_masked,
                alpha=1, edgecolors='face', linewidths=0, marker='s',
                cmap=get_flooding_waterlevel_cmap(),
                vmin=0, vmax=1.5)

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

    img.save(image_file, format='PNG')

def muidsgrid(muids):

    grid2D = {
        "j0": 1751622.5000000084,
        "k0": 5947162.5000000652,
        "numJ": 273,
        "numK": 189,
        "deltaJ": 5.0,
        "deltaK": 5.0
    }

    crs_dhi = 'PROJCS[\"NZGD2000 / New Zealand Transverse Mercator 2000\",GEOGCS[\"NZGD2000\",DATUM[\"New_Zealand_Geodetic_Datum_2000\",'+\
    'SPHEROID[\"GRS 1980\",6378137,298.257222101,AUTHORITY[\"EPSG\",\"7019\"]],TOWGS84[0,0,0,0,0,0,0],AUTHORITY[\"EPSG\",\"6167\"]],'+\
    'PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],' +\
    'AXIS[\"Latitude\",NORTH],AXIS[\"Longitude\",EAST],AUTHORITY[\"EPSG\",\"4167\"]],PROJECTION[\"Transverse_Mercator\"],' +\
    'PARAMETER[\"latitude_of_origin\",0],PARAMETER[\"central_meridian\",173],PARAMETER[\"scale_factor\",0.9996],' +\
    'PARAMETER[\"false_easting\",1600000],PARAMETER[\"false_northing\",10000000],UNIT[\"metre\",1,AUTHORITY[\"EPSG\",\"9001\"]],' +\
    'AUTHORITY[\"EPSG\",\"2193\"]]'
    transformer_dhi3857 = pyproj.Transformer.from_crs(pyproj.CRS.from_epsg(3857), crs_dhi)

    muids1 = np.zeros(muids.shape)

    muids1[:,0], muids1[:, 1] = transformer_dhi3857.transform(muids[:,0], muids[:,1])

    muids1[:,0] -= grid2D['j0']
    muids1[:,1] -= grid2D['k0']

    muids1[:,0] /= grid2D['deltaJ']
    muids1[:,1] /= grid2D['deltaK']

    return muids1

if __name__ == "__main__":

    muids = np.load(os.path.join('tmp', 'muids_3857.npy'))
    data = np.load(os.path.join('tmp', '1666857600.npy'))


    muids1 = muidsgrid(muids)

    # print(muids1)

    _generate_flood_png3857(muids1, data, os.path.join('tmp', 'somefilename.png'))

    