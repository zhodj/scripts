#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,sys
from PIL import Image,ImageFont, ImageDraw
import random

text = ["1","2","3","4","5","6","7","8","9","0"]
di = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"0":0}
def CreatePng(text, seq, path_name, fonts_path):
    im = Image.new("RGB", (28, 28), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", fonts_path), 20)
    dr.text((2, 2), text, font=font, fill="#000000")
    im.show()
    im.save(os.path.join(path_name, text + "_" + ("%05d" % seq) +".jpg"))

def Run(length, path_name, fonts_path):
    for i in range(length):
        num = random.randint(0, 9)
        text = str(num)
        di[text] = di[text] + 1
        CreatePng(str(num), di[text], path_name, fonts_path)
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "need two args!"
        sys.exit(0)
    model = sys.argv[1]
    fonts_path = "msyh.ttf"
    if model == "test":
        length = 10000
        path_name = "test_numbers"
        Run(length, path_name, fonts_path)
    elif model == "train":
        length = 60000
        path_name = "train_numbers"
        Run(length, path_name, fonts_path)

