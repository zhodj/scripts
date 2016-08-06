#!/usr/bin/env python

import os,sys
import cv2
import numpy as np
from struct import *
from ctypes import create_string_buffer

def get_filename(filename):
    v = filename.split("\.")
    s = v[0].split("_")
    return int(s[0])
    
def read_source_files(pathname, out_image, out_label, image_numbers):
    len_image = 16 + 28 * 28 * image_numbers
    len_label = 16 + 1 * image_numbers
    s_image = create_string_buffer(len_image)
    s_label = create_string_buffer(len_label)
    magic_number = 0x00000803;
    magic_label_number = 0x00000801;

    row_numbers = 28;
    col_numbers = 28;
    l_image = 0;
    l_label = 0;

    pack_into('>I', s_image, l_image, magic_number)
    l_image = l_image + 4
    pack_into('>I', s_label, l_label, magic_label_number)
    l_label = l_label + 4

    pack_into('>I', s_image, l_image, image_numbers)
    l_image = l_image + 4

    pack_into('>I', s_label, l_label, image_numbers)
    l_label = l_label + 4

    pack_into('>I', s_image, l_image, row_numbers)
    l_image = l_image + 4
    pack_into('>I', s_image, l_image, col_numbers)
    l_image = l_image + 4

    li = os.listdir(pathname)
    for l in li:
        filepath = os.path.join(pathname, l)
        if not os.path.isdir(filepath):
            label = get_filename(l)
            img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE);
            l = img.shape[0]
            r = img.shape[1]
            for i in xrange(l):
                for j in xrange(r):
                    pack_into('B', s_image, l_image, img[i, j])
                    l_image = l_image + 1
            pack_into('B', s_label, l_label, label)
            l_label = l_label + 1

    with open(out_image, 'wb') as output:
        output.write(s_image)
    output.close()

    with open(out_label, 'wb') as output:
        output.write(s_label)
    output.close()


if __name__ == '__main__':
    model = sys.argv[1]
    pathname = "/home/zhoudingjun/workstation/scripts/python/tensorflow/"
    out_image = ""
    out_label = ""
    if model == "train":
        pathname = pathname + "train_numbers/"
        out_image = 'train-images-idx3-ubyte'
        out_label = 'train-labels-idx1-ubyte'
        image_numbers = 60000
    elif model == "test":
        pathname = pathname + "test_numbers/"
        out_image = 'test-images-idx3-ubyte'
        out_label = 'test-labels-idx1-ubyte'
        image_numbers = 10000

    read_source_files(pathname, out_image, out_label, image_numbers) 
