import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager
import RenderObject
from Input import Input
from Texture import Texture

def main():
  screenSize: (int) = (800, 600)
  renderer: Renderer = Renderer(screenSize)
  renderManager: RenderManager = RenderManager(renderer)
  RenderObject.generate_shapes()

  Input.init(renderer.window)

  glViewport(0, 0, screenSize[0], screenSize[1])
  glClearColor(0x22 / 0xff, 0x00 / 0xff, 0x00 / 0xff, 1)

  glEnable(GL_DEPTH_TEST)

  grapesTex = Texture("grapes.bmp")

  cubes = [RenderObject.Cube(renderer) for _ in range(5000)]
  for i in range(len(cubes)):
    cube = cubes[i]
    renderManager.add_object(cube)
    cube.modelMat = glm.translate(cube.modelMat, glm.vec3(i, 0, 0))
    cube.texture = grapesTex
  bbSquare = RenderObject.SquareBB(renderer)
  renderManager.add_object(bbSquare)
  bbSquare.modelMat = glm.translate(bbSquare.modelMat, glm.vec3(0, 1, 0))
  bbSquare.texture = grapesTex

  projMat = glm.perspective(glm.radians(60), screenSize[0] / screenSize[1], 0.1, 100)
  viewMat = glm.mat4(1)
  
  renderer.swap_program("simple3D")
  renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  renderer.swap_program("billboard")
  renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  camPos = glm.vec3(0, 0, -3)

  frame: int = 0
  while not glfw.window_should_close(renderer.window):
    Input.update()

    speed = 0.5
    if Input.is_held(glfw.KEY_A):
      camPos.x += speed
    if Input.is_held(glfw.KEY_D):
      camPos.x -= speed
    if Input.is_held(glfw.KEY_Q):
      camPos.y += speed
    if Input.is_held(glfw.KEY_E):
      camPos.y -= speed
    if Input.is_held(glfw.KEY_W):
      camPos.z += speed
    if Input.is_held(glfw.KEY_S):
      camPos.z -= speed

    renderManager.camPos = camPos
    renderer.swap_program("simple3D")
    viewMat = glm.lookAt(
      camPos,
      glm.vec3(0, 0, 0),
      glm.vec3(0, 1, 0)
    )
    renderer.set_uniform("viewMat", viewMat)

    renderer.swap_program("billboard")
    renderer.set_uniform("viewMat", viewMat)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    renderManager.draw_all_objects()

    glfw.swap_buffers(renderer.window)
    glfw.poll_events()
    
    frame = frame + 1

  glfw.terminate()

if __name__ == "__main__":
  main()