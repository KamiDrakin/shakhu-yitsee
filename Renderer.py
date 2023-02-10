from OpenGL.GL import *
import glfw
import glm
from typing import Any

shaderDir = "shaders/"

uniformTypes = {
  glm.mat4: lambda x, y: glUniformMatrix4fv(x, 1, GL_FALSE, glm.value_ptr(y)),
  glm.vec4: lambda x, y: glUniform4fv(x, 1, glm.value_ptr(y))
}

class Program:
  def __init__(self, ID: int):
    self.ID: int = ID
    self.uniforms: dict[str, int] = {}

class ScreenSizer:
  fov = 60
  near = 0.1
  far = 64

  def __init__(self, size: tuple[int]):
    self.projMats: dict[int, glm.mat4] = {}
    self.size = size
    self.update_projections(size)

  def update_projections(self, size: tuple[int]):
    self.projMats = {
      0: glm.perspective(glm.radians(self.fov), size[0] / size[1], self.near, self.far),
      1: glm.ortho(0, size[0], 0, size[1], -100, 100)
    }

  def get_projection(self, type: int) -> glm.mat4:
    return self.projMats[type]

  def frame_buffer_size_callback(self, window, width, height):
    if width != 0 and height != 0:
      glViewport(0, 0, width, height)
      self.update_projections((width, height))
      self.size = (width, height)

class Renderer:
  def __init__(self, size: tuple[int]):
    self.programs: dict[str, Program] = {}
    self.currentProgram: str = ""

    self.screenSizer = ScreenSizer(size)

    glfw.init()
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.VISIBLE, False)
    #glfw.window_hint(glfw.RESIZABLE, False)
    
    self.window = glfw.create_window(size[0], size[1], "AAAA", None, None)
    glfw.make_context_current(self.window)
    glfw.swap_interval(1)

    glfw.set_framebuffer_size_callback(self.window, self.screenSizer.frame_buffer_size_callback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)
    glCullFace(GL_BACK)
    glEnable(GL_MULTISAMPLE)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

  def create_program_from_files(self, name: str):
    if name in self.programs:
      return
    file = open(shaderDir + name + "_vert.glsl", "r")
    vertSrc = file.read()
    file.close()
    file = open(shaderDir + name + "_frag.glsl", "r")
    fragSrc = file.read()
    file.close()
    self.create_program(name, vertSrc, fragSrc)

  def create_program(self, name: str, vertSrc: str, fragSrc: str):
    if name in self.programs:
      return
    vertShader: int = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertShader, vertSrc)
    glCompileShader(vertShader)
    if glGetShaderiv(vertShader, GL_COMPILE_STATUS) != GL_TRUE:
      err = glGetShaderInfoLog(vertShader) 
      raise Exception(err)  

    fragShader: int = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragShader, fragSrc)
    glCompileShader(fragShader)
    if glGetShaderiv(fragShader, GL_COMPILE_STATUS) != GL_TRUE:
      err = glGetShaderInfoLog(fragShader) 
      raise Exception(err)  

    program: int = glCreateProgram()
    glAttachShader(program, vertShader)
    glAttachShader(program, fragShader)
    glLinkProgram(program)
    if glGetProgramiv(program, GL_LINK_STATUS) != GL_TRUE:
      err = glGetShaderInfoLog(program) 
      raise Exception(err)

    glDeleteShader(vertShader)
    glDeleteShader(fragShader)    

    self.programs[name] = Program(program)

  def swap_program(self, name: str):
    glUseProgram(self.programs[name].ID)
    self.currentProgram = name

  def define_uniform(self, name: str):
    currProgram = self.programs[self.currentProgram]
    if name not in currProgram.uniforms:
      currProgram.uniforms[name] = glGetUniformLocation(currProgram.ID, name)

  def set_uniform(self, name: str, value: Any):
    uniformTypes[type(value)](self.programs[self.currentProgram].uniforms[name], value)