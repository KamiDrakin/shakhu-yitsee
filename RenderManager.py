from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderObject import RenderObject

maxObjsPerVao = 1024
renderDistance = 64

class VAO:
  def __init__(self):
    self.objCount = 0
    self.programs: dict[str, RenderObject] = {}

class Layer:
  def __init__(self, projectionId: int, distanceCull: bool):
    self.vaos: dict[int, VAO] = {}
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

  def add_object(self, obj: RenderObject, layerId: int = 1):
    vaoId: int = obj.shape.vao
    program: str = obj.program
    vaos: dict[int, VAO] = self.layers[layerId].vaos
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
        self.renderer.set_uniform("projMat", self.renderer.screenSizer.get_projection(layer.projectionId))
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