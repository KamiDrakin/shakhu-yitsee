import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager
import RenderObject
from Input import Input
from Texture import Texture

def follow_behind(pos: glm.vec3, dest: glm.vec3, speed: float, desDist: float):
  if speed > 1:
    speed = 1
  elif speed <= 0:
    return
  diff = dest - pos
  if glm.length(diff.xz) == desDist and abs(diff.y) == glm.length(diff):
    return
  offset = desDist * glm.normalize(diff)
  pos.xz += speed * (diff.xz - offset.xz)

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

  grapeOverlords = [RenderObject.SquareUI(renderer) for _ in range(30)]
  for i in range(len(grapeOverlords)):
    grapeOverlord = grapeOverlords[i]
    grapeOverlord.modelMat = glm.scale(glm.translate(glm.mat4(1), glm.vec3(400, 300, len(grapeOverlords) - i)), glm.vec3(800 / (1 + i), 600 / (1 + i), 0))
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

  camPos = glm.vec3(0, 2.5, -3)
  camTarget = glm.vec3(0, 1.5, 0)
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

    camDir = glm.normalize(camPos - camTarget)
    camRight = glm.normalize(glm.cross(glm.vec3(0, 1, 0), camDir))
    camUp = glm.normalize(glm.cross(camDir, camRight))
    playerRight = glm.normalize(camRight.xz)
    playerForward = glm.normalize(glm.cross(camRight, glm.vec3(0, 1, 0)).xz)

    if Input.is_held(glfw.KEY_Z):
      playerPos.y += speed
      camPos.y += speed
    if Input.is_held(glfw.KEY_X):
      playerPos.y -= speed
      camPos.y -= speed

    playerMovement = glm.vec2(0)

    if Input.is_held(glfw.KEY_A):
      playerMovement.xy -= playerRight
    if Input.is_held(glfw.KEY_D):
      playerMovement.xy += playerRight
    if Input.is_held(glfw.KEY_W):
      playerMovement.xy -= playerForward
    if Input.is_held(glfw.KEY_S):
      playerMovement.xy += playerForward

    camMoved = False
    if Input.is_held(glfw.KEY_Q):
      camPos += speed * camRight
      camMoved = True
    if Input.is_held(glfw.KEY_E):
      camPos -= speed * camRight
      camMoved = True
    if Input.is_held(glfw.KEY_R):
      if glm.acos(glm.dot(camUp, glm.vec3(playerForward.x, 0, playerForward.y))) > glm.pi() / 4:
        camPos -= speed * camUp
    if Input.is_held(glfw.KEY_F):
      if glm.acos(glm.dot(camUp, glm.vec3(playerForward.x, 0, playerForward.y))) < glm.pi() * 3 / 4:
        camPos += speed * camUp

    if playerMovement != glm.vec2(0):
      playerPos.xz += speed * glm.normalize(playerMovement)
      if camMoved:
        camPos.xz += speed * glm.normalize(playerMovement)
    
    bbSquare.modelMat = glm.translate(glm.mat4(1), playerPos)
      
    camTarget.y = playerPos.y
    follow_behind(camTarget, playerPos, 0.2, 0)
    follow_behind(camPos, camTarget, 1, 3)
    
    for i in range(len(grapeOverlords)):
      grapeOverlord = grapeOverlords[i]
      grapeOverlord.modelMat = glm.scale(
        glm.translate(
          glm.mat4(1),
          glm.vec3(
            renderer.screenSizer.size[0] / 2,
            renderer.screenSizer.size[1] / 2,
            i
          )
        ), 
        glm.vec3(renderer.screenSizer.size[0] / (1 + i / 3) ** glm.sin(glfw.get_time()), renderer.screenSizer.size[1] / (1 + i / 3) ** glm.sin(glfw.get_time()), 1)
      )

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

    glClear(GL_COLOR_BUFFER_BIT)
    renderManager.draw_all_objects()
    glfw.swap_buffers(renderer.window)
    glfw.poll_events()

  glfw.terminate()

if __name__ == "__main__":
  main()