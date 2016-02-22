# Pytrack
### Low Cost, Open Source Object Tracking on Raspberry Pi

This repository contains work from the Open Tracking (CS Capstone 32) group, specifically Pytrack.  Pytrack uses a Raspberry Pi, camera, and DC motors to easily and cheaply track faces.  

To run an example of facial detection, run `python test.py cascade/haarcascade_frontalface_default.xml`.  OpenCV must be installed for this to run.  

### One-command installation

check out the install script we have at https://github.com/opentracking/pytrack/install.sh and make sure you trust it! Then run the following command:
This will use apt-get (to make sure python-opencv is installed), so it will need sudo permissions. It will then attempt to run our test program.
 
wget -0 - https://github.com/opentracking/pytrack/install.sh