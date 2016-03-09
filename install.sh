#!/bin/bash
apt-get update
apt-get install python-opencv -y
apt-get install libgli-mesa-*
ldconfig
git clone https://github.com/opentracking/pytrack.git pytrack_example
cd pytrack_example
python test.py cascade/haarcascade_frontalface_default.xml

