from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderObject import RenderObject

maxObjsPerVao = 128
renderDistance = 64

class VAO:
  def __init__(self):
    self.objCount = 0
    self.programs: dict[str, RenderObject] = {}

class RenderManager:
  def __init__(self, renderer: Renderer):
    self.renderer = renderer
    #grouped by projection -> vao -> program
    bgObjs: dict[int, dict[int, VAO]] = {}
    worldObjs: dict[int, dict[int, VAO]] = {}
    fgObjs: dict[int, dict[int, VAO]] = {}
    self.layers = (bgObjs, worldObjs, fgObjs)
    self.layerProjections = (1, 0, 1)
    self.camPos = glm.vec3(0)

  def add_object(self, obj: RenderObject, layer: int = 1):
    vaoId: int = obj.shape.vao
    program: str = obj.program
    vaos: dict[int, VAO] = self.layers[layer]
    if vaoId not in vaos:
      vaos[vaoId] = VAO()
    vaos[vaoId].objCount += 1
    programs: dict[str, list[RenderObject]] = vaos[vaoId].programs
    if obj.program not in programs:
      programs[program] = []
    programs[program].append(obj)

  def draw_all_objects(self):
    glDisable(GL_DEPTH_TEST)
    self.draw_layer(0)
    glEnable(GL_DEPTH_TEST)
    self.draw_layer(1)
    glDisable(GL_DEPTH_TEST)
    self.draw_layer(2)

  def draw_layer(self, id: int):
    vaos: dict[int, VAO] = self.layers[id]
    for vao in vaos:
      maxObjs = maxObjsPerVao
      glBindVertexArray(vao)
      programs: dict[str, list[RenderObject]] = vaos[vao].programs
      for program in programs:
        self.renderer.swap_program(program)
        self.renderer.set_uniform("projMat", self.renderer.screenSizer.get_projection(self.layerProjections[id]))
        objs: list[RenderObject] = programs[program]
        toRender = len(objs)
        if maxObjs < toRender:
          toRender = maxObjs
          if toRender < 0:
            toRender = 0
          print("VAO limit exceeded.")
        else:
          maxObjs -= toRender
        for i in range(toRender):
          obj = objs[i]
          if id == 1 and glm.distance(glm.vec3(obj.modelMat[3]), self.camPos) > renderDistance:
            continue
          obj.draw()