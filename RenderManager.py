from OpenGL.GL import *

from Renderer import Renderer
from RenderObject import RenderObject

class RenderManager:
  def __init__(self, renderer: Renderer):
    self.renderer = renderer
    self.loadedObjs: dict[int, dict[str, list[RenderObject]]] = {}

  def add_object(self, obj: RenderObject):
    vao: int = obj.shape.vao
    if vao not in self.loadedObjs:
      self.loadedObjs[vao] = {}
    program: str = obj.program
    if obj.program not in self.loadedObjs[vao]:
      self.loadedObjs[vao][program] = []
    self.loadedObjs[vao][program].append(obj)

  def draw_all_objects(self):
    for vao in self.loadedObjs:
      glBindVertexArray(vao)
      for program in self.loadedObjs[vao]:
        self.renderer.swap_program(program)
        objs: list[RenderObject] = self.loadedObjs[vao][program]
        for obj in objs:
          obj.draw()