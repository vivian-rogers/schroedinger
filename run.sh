#!/bin/bash

mkdir results
rm ./results/slice*.png
rm ./results/test.mp4

python3 hamiltonian.py

#bash plotslice.sh
bash ./render.sh 24
#cp results/test.mp4 ./render.mp4



