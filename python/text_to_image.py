#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import Image,ImageFont, ImageDraw
import random

text = ["1","2","3","4","5","6","7","8","9","0"]
di = {"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"0":0}
def CreatePng(text, seq):
    im = Image.new("RGB", (28, 28), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "msyh.ttf"), 20)
    dr.text((2, 2), text, font=font, fill="#000000")
    im.show()
    im.save(os.path.join("test_numbers", text + "_" + ("%05d" % seq) +".jpg"))

def Run():
    for i in range(10000):
        num = random.randint(0, 9)
        text = str(num)
        di[text] = di[text] + 1
        CreatePng(str(num), di[text])
Run()
        
