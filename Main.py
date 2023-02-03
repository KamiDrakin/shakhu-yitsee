import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager
import RenderObject
from Input import Input

def main():
  screenSize: (int) = (800, 600)
  renderer: Renderer = Renderer(screenSize)
  renderManager: RenderManager = RenderManager(renderer)
  RenderObject.generate_shapes()

  Input.init(renderer.window)

  glViewport(0, 0, screenSize[0], screenSize[1])
  glClearColor(0x22 / 0xff, 0x00 / 0xff, 0x00 / 0xff, 1)

  glEnable(GL_DEPTH_TEST)

  cubes = [RenderObject.Cube(renderer) for _ in range(500)]
  for i in range(len(cubes)):
    cube = cubes[i]
    renderManager.add_object(cube)
    cube.modelMat = glm.translate(cube.modelMat, glm.vec3(i, 0, 0))
  bbSquare = RenderObject.SquareBB(renderer)
  renderManager.add_object(bbSquare)
  bbSquare.modelMat = glm.translate(bbSquare.modelMat, glm.vec3(0, 1, 0))

  projMat = glm.perspective(glm.radians(60), screenSize[0] / screenSize[1], 0.1, 100)
  viewMat = glm.mat4(1)
  
  renderer.swap_program("simple3D")
  renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  renderer.swap_program("billboard")
  renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  camX: int = 0
  camY: int = 0
  camZ: int = -3

  frame: int = 0
  while not glfw.window_should_close(renderer.window):
    Input.update()

    speed = 1
    if Input.is_held(glfw.KEY_A):
      camX += speed
    if Input.is_held(glfw.KEY_D):
      camX -= speed
    if Input.is_held(glfw.KEY_Q):
      camY += speed
    if Input.is_held(glfw.KEY_E):
      camY -= speed
    if Input.is_held(glfw.KEY_W):
      camZ += speed
    if Input.is_held(glfw.KEY_S):
      camZ -= speed

    renderer.swap_program("simple3D")
    viewMat = glm.lookAt(
      glm.vec3(camX, camY, camZ),
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