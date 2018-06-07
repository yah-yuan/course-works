import numpy
from PIL import Image

img = Image.open('Lenna.jpg','r')
img.convert()
img.show()
a = numpy.array(img)
print(a)