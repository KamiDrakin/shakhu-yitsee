from OpenGL.GL import *
from ctypes import sizeof, c_void_p
import numpy

import SimpleModels as sMod

class Shape:
  def __init__(self):
    self.vao: int = glGenVertexArrays(1)
    self.vbo: int = glGenBuffers(1)

  def draw(self):
    print("Draw function has not been overriden.")

class Cube(Shape):
  def __init__(self):
    super().__init__()
    glBindVertexArray(self.vao)
    glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    glBufferData(GL_ARRAY_BUFFER, numpy.array(sMod.cubeFull, dtype='float32'), GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), c_void_p(3 * sizeof(GLfloat)))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

  def draw(self):
    glDrawArrays(GL_TRIANGLES, 0, 36)

class Square(Shape):
  def __init__(self):
    super().__init__()
    glBindVertexArray(self.vao)
    glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
    glBufferData(GL_ARRAY_BUFFER, numpy.array(sMod.squareFull, dtype='float32'), GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), c_void_p(0))
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 6 * sizeof(GLfloat), c_void_p(3 * sizeof(GLfloat)))
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

  def draw(self):
    glDrawArrays(GL_TRIANGLES, 0, 6)