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

start = time.time()

# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Stitch plots',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('dir',
                        metavar='str',
                        nargs='+',
                        help='Directory in which plot subdirectories are located')

    return parser.parse_args()


def process_dir(subdire):
        start2 = time.time()

        plot = subdire.split('/')[-1]
        plot_split = plot.split(' ')
        cwd = os.getcwd()
        plot_name = '_'.join(plot_split)

        os.chdir(subdire)

        images = glob.glob('*.tif', recursive=True)

        img_list = []
        for i in images:
            image = i.split('/')[-1]
            img_list.append(image)
        img_str = ' '.join(img_list)

        cmd = f'gdalbuildvrt mosaic.vrt {img_str}'
        subprocess.call(cmd, shell=True)

        cmd2 = f'gdal_translate -co COMPRESS=LZW -co BIGTIFF=YES -outsize 100% 100% mosaic.vrt {plot_name}_ortho.tif'
        subprocess.call(cmd2, shell=True)

# --------------------------------------------------
def main():
    """Run 'orthomosaic' here"""

    args = get_args()

    start = time.time()

    with multiprocessing.Pool(multiprocessing.cpu_count()) as p:
        p.map(process_dir, args.dir)

    end = time.time()
    total_time = end - start
    print(f'Done - Processing time: {total_time} seconds.')


# --------------------------------------------------
if __name__ == '__main__':
    main()
