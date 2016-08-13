#!/usr/bin/python

import gzip
import sys

import numpy
from tensorflow.python.platform import gfile

def _read32(bytestream):
    dt = numpy.dtype(numpy.uint32).newbyteorder('>')
    return numpy.frombuffer(bytestream.read(4), dtype=dt)[0]

def dense_to_one_hot(labels_dense, num_classes):
      """Convert class labels from scalars to one-hot vectors."""
      num_labels = labels_dense.shape[0]
      index_offset = numpy.arange(num_labels) * num_classes
      labels_one_hot = numpy.zeros((num_labels, num_classes))
      labels_one_hot.flat[index_offset + labels_dense.ravel()] = 1
      return labels_one_hot

def extract_images(filename):
    """Extract the images into a 4D uint8 numpy array [index, y, x, depth]."""
    print('Extracting', filename)
    with gfile.Open(filename, 'rb') as f, gzip.GzipFile(fileobj=f) as bytestream:
        magic = _read32(bytestream)
        if magic != 2051:
            raise ValueError('Invalid magic number %d in MNIST image file: %s' % (magic, filename))
        num_images = _read32(bytestream)
        print num_images
        rows = _read32(bytestream)
        cols = _read32(bytestream)
        print rows, cols
        buf = bytestream.read(rows * cols * num_images)
        data = numpy.frombuffer(buf, dtype=numpy.uint8)
        print len(data)
        data = data.reshape(num_images, rows, cols, 1)
        return data

def extract_labels(filename, one_hot=False, num_classes=10):
      """Extract the labels into a 1D uint8 numpy array [index]."""
      print('Extracting', filename)
      with gfile.Open(filename, 'rb') as f, gzip.GzipFile(fileobj=f) as bytestream:
        magic = _read32(bytestream)
        if magic != 2049:
            raise ValueError('Invalid magic number %d in MNIST label file: %s' %
                                                               (magic, filename))
        num_items = _read32(bytestream)
        buf = bytestream.read(num_items)
        labels = numpy.frombuffer(buf, dtype=numpy.uint8)
        if one_hot:
            return dense_to_one_hot(labels, num_classes)
        return labels

path1 = sys.argv[1]
path2 = sys.argv[2]
extract_images(path1)
extract_labels(path2)
