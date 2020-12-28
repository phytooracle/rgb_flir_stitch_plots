#!/usr/bin/env python3
"""
Author : Emmanuel Gonzalez
Date   : 2020-04-11
Purpose: Stitch geo-corrected images into plot 'orthos'
"""

import argparse
import os
import glob
import subprocess
import time
import multiprocessing
from osgeo import gdal

start = time.time()

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Stitch plots',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='str',
                        help='Directory in which plot subdirectories are located')

    return parser.parse_args()


def process_dir(subdir):

    start2 = time.time()

    plot = subdir.split('/')[-1]
    plot_split = plot.split(' ')
    cwd = os.getcwd()
    plot_name = '_'.join(plot_split)

    vrt_options = gdal.BuildVRTOptions(srcNodata="0 0 0",
                                   resampleAlg='cubic',
                                   addAlpha=False)

    # Create VRT
    os.chdir(subdir)
    images = glob.glob('*.tif')
    vrt = gdal.BuildVRT('my.vrt', images, options=vrt_options)

    # Create geoTiff from VRT
    translateOptions = gdal.TranslateOptions(creationOptions=["TILED=YES",
                                                              "COMPRESS=LZW",
                                                              "BIGTIFF=YES"])
    gdal.Translate(f'{plot_name}.tif', vrt, driver="GTiff", options=translateOptions)
    vrt = None


# --------------------------------------------------
def main():
    """Run 'orthomosaic' here"""

    args = get_args()

    start = time.time()

    directories = glob.glob(args.dir + '*')

    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(process_dir, directories)

    end = time.time()
    total_time = end - start
    print(f'Done - Processing time: {total_time} seconds.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
