from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderObject import RenderObject

renderDistance: float = 100

class RenderManager:
  def __init__(self, renderer: Renderer):
    self.renderer = renderer
    #grouped by projection -> vao -> program
    bgObjs: dict[int, dict[int, dict[str, list[RenderObject]]]] = {}
    worldObjs: dict[int, dict[int, dict[str, list[RenderObject]]]] = {}
    fgObjs: dict[int, dict[int, dict[str, list[RenderObject]]]] = {}
    self.layers = (bgObjs, worldObjs, fgObjs)
    self.layerProjections = (1, 0, 1)
    self.camPos = glm.vec3(0)

  def add_object(self, obj: RenderObject, layer: int = 1):
    vao: int = obj.shape.vao
    program: str = obj.program
    vaos = self.layers[layer]
    if vao not in vaos:
      vaos[vao] = {}
    programs = vaos[vao]
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
    vaos = self.layers[id]
    for vao in vaos:
      glBindVertexArray(vao)
      programs = vaos[vao]
      for program in programs:
        self.renderer.swap_program(program)
        self.renderer.set_uniform("projMat", self.renderer.screenSizer.get_projection(self.layerProjections[id]))
        objs: list[RenderObject] = programs[program]
        for obj in objs:
          if id == 1 and glm.distance(glm.vec3(obj.modelMat[3]), self.camPos) > renderDistance:
            continue
          obj.draw()