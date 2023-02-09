import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager
import RenderObject
from Input import Input
from Texture import Texture

def follow_behind(pos: glm.vec3, dest: glm.vec3, speed: float, desDist: float, desHeight: float, acceleration: float = 2):
  dist = glm.distance(dest.xz, pos.xz)
  distDiff = glm.abs(dist - desDist)
  hSpeed = speed * distDiff ** acceleration
  if hSpeed > distDiff:
    hSpeed = distDiff
  if desDist < dist:
    pos.xz += hSpeed * glm.normalize(dest.xz - pos.xz)
  elif desDist > dist:
    pos.xz += hSpeed * glm.normalize(pos.xz - dest.xz)
  height = pos.y - dest.y
  heightDiff = glm.abs(height - desHeight)
  vSpeed = speed * heightDiff ** acceleration
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

  cubes = [[RenderObject.Cube(renderer) for _ in range(10)] for _ in range(10)]
  for z in range(len(cubes)):
    for x in range(len(cubes[z])):
      cube = cubes[z][x]
      renderManager.add_object(cube)
      cube.modelMat = glm.translate(cube.modelMat, glm.vec3(x, 0, z))
      cube.texture = grapesTex

  square1 = RenderObject.Square3D(renderer)
  square1.modelMat = glm.rotate(square1.modelMat, glm.radians(180), glm.vec3(0, 1, 0))
  square1.modelMat = glm.translate(square1.modelMat, glm.vec3(-4.5, 5.5, -9.5))
  square1.modelMat = glm.scale(square1.modelMat, glm.vec3(10, 10, 1))
  square1.texture = grapesTex
  renderManager.add_object(square1)

  square2 = RenderObject.Square3D(renderer)
  square2.modelMat = glm.rotate(square2.modelMat, glm.radians(-90), glm.vec3(0, 1, 0))
  square2.modelMat = glm.translate(square2.modelMat, glm.vec3(4.5, 5.5, -9.5))
  square2.modelMat = glm.scale(square2.modelMat, glm.vec3(10, 10, 1))
  square2.texture = grapesTex
  renderManager.add_object(square2)

  bbSquare = RenderObject.SquareBB(renderer)
  bbSquare.modelMat = glm.translate(bbSquare.modelMat, glm.vec3(0, 1, 0))
  bbSquare.texture = grapesTex
  renderManager.add_object(bbSquare)

  grapeOverlord = RenderObject.SquareUI(renderer)
  grapeOverlord.modelMat = glm.translate(glm.scale(glm.mat4(1), glm.vec3(800, 600, 1)), glm.vec3(0.5, 0.5, 0))
  grapeOverlord.texture = grapesTex
  renderManager.add_object(grapeOverlord, 0)

  viewMat = glm.mat4(1)
  
  renderer.swap_program("simple3D")
  renderer.set_uniform("viewMat", viewMat)
  renderer.set_uniform("colorFilter", glm.vec4(1, 0, 1, 1))

  renderer.swap_program("billboard")
  renderer.set_uniform("viewMat", viewMat)
  renderer.set_uniform("colorFilter", glm.vec4(1, 0, 1, 1))

  renderer.swap_program("ui")
  renderer.set_uniform("colorFilter", glm.vec4(1, 0, 1, 1))

  camPos = glm.vec3(0, 0, -3)
  camHeight = 1.5
  camTarget = glm.vec3(0, 2, 0)
  playerPos = glm.vec3(0, 1, 0)

  frames = 0
  totalTime = 0
  time = glfw.get_time()
  while not glfw.window_should_close(renderer.window):
    Input.update()
    
    prevTime = time
    time = glfw.get_time()
    delta = time - prevTime
    totalTime += delta
    frames += 1
    if totalTime > 10:
      totalTime -= 10
      print(frames / 10)
      frames = 0

    speed = 5 * delta
    follow_behind(camTarget, playerPos, 2 * speed, 0, 0.5)
    camDir = glm.normalize(camPos - camTarget)
    camRight = glm.normalize(glm.cross(glm.vec3(0, 1, 0), camDir))
    camUp = glm.normalize(glm.cross(camDir, camRight))
    playerRight = glm.normalize(camRight.xz)
    playerForward = glm.normalize(glm.cross(camRight, glm.vec3(0, 1, 0)))

    if Input.is_held(glfw.KEY_A):
      playerPos.xz -= speed * playerRight
    if Input.is_held(glfw.KEY_D):
      playerPos.xz += speed * playerRight
    if Input.is_held(glfw.KEY_Q):
      playerPos.y += speed
    if Input.is_held(glfw.KEY_E):
      playerPos.y -= speed
    if Input.is_held(glfw.KEY_W):
      playerPos.xz -= speed * playerForward.xz
    if Input.is_held(glfw.KEY_S):
      playerPos.xz += speed * playerForward.xz
    
    bbSquare.modelMat = glm.translate(glm.mat4(1), playerPos)

    if Input.is_held(glfw.KEY_KP_4):
      camPos += speed * camRight
    if Input.is_held(glfw.KEY_KP_6):
      camPos -= speed * camRight
    if Input.is_held(glfw.KEY_KP_8):
      #camPos -= speed * camUp
      camHeight -= speed
    if Input.is_held(glfw.KEY_KP_2):
      #camPos += speed * camUp
      camHeight += speed

    if camHeight > 3:
      camHeight = 3
    if camHeight < -3:
      camHeight = -3

    follow_behind(camPos, camTarget, 2 * speed, 3, camHeight)
    
    grapeOverlord.modelMat = glm.translate(glm.scale(glm.mat4(1), glm.vec3(renderer.screenSizer.size[0], renderer.screenSizer.size[1], 1)), glm.vec3(0.5, 0.5, 0))

    renderManager.camPos = camPos
    viewMat = glm.lookAt(
      camPos,
      camTarget,
      glm.vec3(0, 1, 0)
    )
    renderer.swap_program("simple3D")
    renderer.set_uniform("viewMat", viewMat)

    renderer.swap_program("billboard")
    renderer.set_uniform("viewMat", viewMat)

    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    glEnable(GL_DEPTH_TEST)
    renderManager.draw_all_objects()

    glfw.swap_buffers(renderer.window)
    glfw.poll_events()

  glfw.terminate()

if __name__ == "__main__":
  main()