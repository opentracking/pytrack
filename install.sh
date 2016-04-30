#!/bin/bash
if [[ $1 == "rm" ]]; then
    apt-get update
    apt-get remove python-opencv -y
    ldconfig
else
    apt-get update
    apt-get install python-opencv -y
    apt-get install libgl1-mesa-*
    ldconfig
    git clone https://github.com/opentracking/pytrack.git pytrack_example
    cd pytrack_example
    python test.py cascade/haarcascade_frontalface_default.xml
fi

