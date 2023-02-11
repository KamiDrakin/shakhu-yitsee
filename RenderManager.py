from OpenGL.GL import *
import glm
import numpy

from Renderer import Renderer
from RenderObject import RenderObject
from Texture import Texture

maxObjsPerVao = 1024
renderDistance = 64

class VAO:
  def __init__(self):
    self.objCount = 0
    self.programs: dict[str, RenderObject] = {}

class Layer:
  def __init__(self, projectionId: int, distanceCull: bool):
    self.vaos: dict[int, VAO] = {}
    self.customProjection: glm.mat4 = None
    self.projectionId = projectionId
    self.distanceCull = distanceCull

class RenderManager:
  def __init__(self, renderer: Renderer):
    self.renderer = renderer
    #grouped by projection -> vao -> program
    self.layers = (
      Layer(1, False),
      Layer(0, True),
      Layer(1, False)
    )
    self.camPos = glm.vec3(0)

  def add_object(self, obj: RenderObject, layer: int|Layer = 1):
    vaoId: int = obj.shape.vao
    program: str = obj.program
    if type(layer) == int:
      layer = self.layers[layer]
    vaos: dict[int, VAO] = layer.vaos
    if vaoId not in vaos:
      vaos[vaoId] = VAO()
    vaos[vaoId].objCount += 1
    programs: dict[str, list[RenderObject]] = vaos[vaoId].programs
    if obj.program not in programs:
      programs[program] = []
    programs[program].append(obj)

  def draw_all_objects(self):
    for layer in self.layers:
      glClear(GL_DEPTH_BUFFER_BIT)
      self.draw_layer(layer)

  def draw_layer(self, layer: Layer):
    vaos: dict[int, VAO] = layer.vaos
    for vao in vaos:
      maxObjs = maxObjsPerVao
      glBindVertexArray(vao)
      programs: dict[str, list[RenderObject]] = vaos[vao].programs
      for program in programs:
        self.renderer.swap_program(program)
        if layer.customProjection == None:
          self.renderer.set_uniform("projMat", self.renderer.screenSizer.get_projection(layer.projectionId))
        else:
          self.renderer.set_uniform("projMat", layer.customProjection)
        objs: list[RenderObject] = programs[program]
        toRender = len(objs)
        if maxObjs < toRender:
          toRender = maxObjs
          if toRender < 0:
            toRender = 0
        else:
          maxObjs -= toRender
        for i in range(toRender):
          obj = objs[i]
          if layer.distanceCull and (glm.distance(glm.vec3(obj.modelMat[3]), self.camPos) > renderDistance):
            continue
          obj.draw()

  def draw_layer_onto_texture(self, layer: Layer, texture: Texture, clear: bool = True):
    fbo = glGenFramebuffers(1)
    glBindFramebuffer(GL_FRAMEBUFFER, fbo)
    glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, texture.id, 0)

    rbo = glGenRenderbuffers(1)
    glBindRenderbuffer(GL_RENDERBUFFER, rbo)
    glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, texture.size[0], texture.size[1])
    glBindRenderbuffer(GL_RENDERBUFFER, 0)
    glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)

    glViewport(0, 0, texture.size[0], texture.size[1])
    if clear:
      glClearColor(1, 0, 1, 1)
      glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)
    self.draw_layer(layer)
    glBindFramebuffer(GL_FRAMEBUFFER, 0)
    glViewport(0, 0, self.renderer.screenSizer.size[0], self.renderer.screenSizer.size[1])
    glDeleteFramebuffers(1, numpy.array(fbo))