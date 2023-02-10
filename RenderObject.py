import glm

from Renderer import Renderer
import Shape
from Texture import Texture

def generate_shapes():
  global shapes
  shapes = {
    "cube": Shape.Cube(),
    "square": Shape.Square()
  }

class RenderObject:
  def __init__(self, renderer: Renderer, program: str):
    self.program: str = program
    self.renderer = renderer
    self.renderer.create_program_from_files(self.program)
    self.shape: Shape.Shape = None
    self.texture: Texture = None
    self.modelMat = glm.mat4(1.0)
    self.colorFilter = glm.vec4(1.0)
    renderer.swap_program(program)
    renderer.define_uniform("modelMat")
    renderer.define_uniform("viewMat")
    renderer.define_uniform("projMat")
    renderer.define_uniform("colorFilter")

  def draw(self):
    self.renderer.set_uniform("colorFilter", self.colorFilter)
    self.renderer.set_uniform("modelMat", self.modelMat)
    self.texture.bind()
    self.shape.draw()

class Cube(RenderObject):
  def __init__(self, renderer: Renderer):
    super().__init__(renderer, "simple3D")
    self.shape = shapes["cube"]

class Square3D(RenderObject):
  def __init__(self, renderer: Renderer):
    super().__init__(renderer, "simple3D")
    self.shape = shapes["square"]

class SquareBB(RenderObject):
  def __init__(self, renderer: Renderer):
    super().__init__(renderer, "billboard")
    self.shape = shapes["square"]

class SquareUI(RenderObject):
  def __init__(self, renderer: Renderer):
    super().__init__(renderer, "ui")
    self.shape = shapes["square"]