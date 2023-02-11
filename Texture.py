from OpenGL.GL import *
from PIL import Image, ImageOps
import numpy

texDir = "textures/"

class Texture:
  def __init__(self, *args):
    self.id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    if type(args[0]) == str:
      img = Image.open(texDir + args[0])
      img = ImageOps.flip(img)
      data = numpy.array(list(img.getdata()), numpy.int8)
      self.size = (img.width, img.height)
      img.close()
    elif type(args[0]) == int and type(args[1]) == int:
      data = numpy.uint8(0)
      self.size = (args[0], args[1])
    else:
      return
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.size[0], self.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glGenerateMipmap(GL_TEXTURE_2D)

  def bind(self):
    glBindTexture(GL_TEXTURE_2D, self.id)