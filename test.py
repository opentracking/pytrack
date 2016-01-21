from pytrack import ImageProcessor

improc = ImageProcessor("cascade/haarcascade_frontalface_default.xml")
improc.findFaces()