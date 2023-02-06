import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager
import RenderObject
from Input import Input
from Texture import Texture

def follow_behind(pos: glm.vec3, dest: glm.vec3, speed: float, desDist: float, desHeight: float):
  dist = glm.distance(dest.xz, pos.xz)
  distDiff = glm.abs(dist - desDist)
  hSpeed = speed * distDiff ** 2
  if hSpeed > distDiff:
    hSpeed = distDiff
  if desDist < dist:
    pos.xz += hSpeed * glm.normalize(dest.xz - pos.xz)
  elif desDist > dist:
    pos.xz += hSpeed * glm.normalize(pos.xz - dest.xz)
  height = pos.y - dest.y
  heightDiff = glm.abs(height - desHeight)
  vSpeed = speed * heightDiff ** 2
  if vSpeed > heightDiff:
    vSpeed = heightDiff
  if desHeight < height:
    pos.y -= vSpeed
  elif desHeight > height:
    pos.y += vSpeed

def main():
  screenSize: (int) = (800, 600)
  renderer: Renderer = Renderer(screenSize)
  renderer.screenSizer.update_projections(screenSize)
  renderManager: RenderManager = RenderManager(renderer)
  RenderObject.generate_shapes()

  Input.init(renderer.window)

  glViewport(0, 0, screenSize[0], screenSize[1])
  glClearColor(0x22 / 0xff, 0x00 / 0xff, 0x00 / 0xff, 1)

  grapesTex = Texture("grapes.bmp")

  cubes = [RenderObject.Cube(renderer) for _ in range(50)]
  for i in range(len(cubes)):
    cube = cubes[i]
    renderManager.add_object(cube)
    cube.modelMat = glm.translate(cube.modelMat, glm.vec3(i, 0, 0))
    cube.texture = grapesTex
  square = RenderObject.Square3D(renderer)
  square.modelMat = glm.translate(square.modelMat, glm.vec3(0, 0, 2))
  square.modelMat = glm.scale(square.modelMat, glm.vec3(100, 100, 1))
  square.texture = grapesTex
  renderManager.add_object(square)
  bbSquare = RenderObject.SquareBB(renderer)
  bbSquare.modelMat = glm.translate(bbSquare.modelMat, glm.vec3(0, 1, 0))
  bbSquare.texture = grapesTex
  renderManager.add_object(bbSquare)

  #projMat = renderer.projMat
  viewMat = glm.mat4(1)
  
  renderer.swap_program("simple3D")
  #renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  renderer.swap_program("billboard")
  #renderer.set_uniform("projMat", projMat)
  renderer.set_uniform("viewMat", viewMat)

  camPos = glm.vec3(0, 0, -3)
  playerPos = glm.vec3(0, 1, 0)

  frame: int = 0
  while not glfw.window_should_close(renderer.window):
    Input.update()

    speed = 0.2
    if Input.is_held(glfw.KEY_A):
      playerPos.x += speed
    if Input.is_held(glfw.KEY_D):
      playerPos.x -= speed
    if Input.is_held(glfw.KEY_Q):
      playerPos.y += speed
    if Input.is_held(glfw.KEY_E):
      playerPos.y -= speed
    if Input.is_held(glfw.KEY_W):
      playerPos.z += speed
    if Input.is_held(glfw.KEY_S):
      playerPos.z -= speed
    
    bbSquare.modelMat = glm.translate(glm.mat4(1), playerPos)

    if Input.is_held(glfw.KEY_KP_4):
      camPos.x += speed
    if Input.is_held(glfw.KEY_KP_6):
      camPos.x -= speed
    if Input.is_held(glfw.KEY_KP_8):
      camPos.z += speed
    if Input.is_held(glfw.KEY_KP_2):
      camPos.z -= speed

    follow_behind(camPos, playerPos, 0.05, 3, 1.5)

    renderManager.camPos = camPos
    viewMat = glm.lookAt(
      camPos,
      playerPos + glm.vec3(0, 0.5, 0),
      glm.vec3(0, 1, 0)
    )
    renderer.swap_program("simple3D")
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