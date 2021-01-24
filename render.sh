#!/bin/bash

cd ./results/
ffmpeg -r $1 -f image2 -s 1200x900 -i slice%d.png -vcodec libx264 -crf 25  -pix_fmt yuv420p test.mp4
cp test.mp4 ../render.mp4

