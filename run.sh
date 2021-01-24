#!/bin/bash

rm ./results/*.tx*
rm ./results/slice*.png
rm ./results/test.mp4

python3 perturb.py

#bash plotslice.sh
bash ./render.sh 24
#cp results/test.mp4 ./render.mp4



