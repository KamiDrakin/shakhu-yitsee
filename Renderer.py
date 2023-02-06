from OpenGL.GL import *
import glfw
import glm

shaderDir = "shaders/"

fov = 60
near = 0.1
far = 100

class Program:
  def __init__(self, ID: int):
    self.ID: int = ID
    self.uniforms: dict[str, int] = {}

class Renderer:
  windowSizeChangeFlag: bool = False

  def __init__(self, size: tuple[int]):
    self.programs: dict[str, Program] = {}
    self.currentProgram: str = ""
    glfw.init()
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.RESIZABLE, False)
    
    self.window = glfw.create_window(size[0], size[1], "AAAA", None, None)
    glfw.make_context_current(self.window)
    glfw.swap_interval(1)
    glfw.set_framebuffer_size_callback(self.window, self.frame_buffer_size_callback)
    
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)
    
    self.update_projection(size[0], size[1])

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

  def set_uniform(self, name: str, value: glm.mat4):
    currProgram: Program = self.programs[self.currentProgram]
    if name not in currProgram.uniforms.keys():
      currProgram.uniforms[name] = glGetUniformLocation(currProgram.ID, name)
    glUniformMatrix4fv(currProgram.uniforms[name], 1, GL_FALSE, glm.value_ptr(value))

  def update_projection(self, width: float, height: float):
    self.projMat = glm.perspective(glm.radians(fov), width / height, near, far)

  def frame_buffer_size_callback(self, window, width, height):
    if width != 0 and height != 0:
      glViewport(0, 0, width, height)
      self.update_projection(width, height)