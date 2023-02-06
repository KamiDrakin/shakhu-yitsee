from OpenGL.GL import *
from PIL import Image, ImageOps
import numpy

texDir = "textures/"

class Texture:
  def __init__(self, name: str):
    img = Image.open(texDir + name)
    img = ImageOps.flip(img)
    data = numpy.array(list(img.getdata()), numpy.int8)
    self.id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, self.id)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, data)
    glGenerateMipmap(GL_TEXTURE_2D)
    img.close()
  
  def bind(self):
    glBindTexture(GL_TEXTURE_2D, self.id)