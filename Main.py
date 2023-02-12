import glfw
from OpenGL.GL import *
import glm

from Renderer import Renderer
from RenderManager import RenderManager, Layer
import RenderObject
from Input import Input
from Texture import Texture
from SheetTexture import SheetTexture

def follow_behind_xz(pos: glm.vec3, dest: glm.vec3, desDist: float, accelerate: bool) -> glm.vec2:
  diff = dest - pos
  if glm.length(diff.xz) == desDist and abs(diff.y) == glm.length(diff):
    return glm.vec2(0)
  offset = desDist * glm.normalize(diff)
  distance = glm.length(diff.xz)
  accelerator = (desDist - distance) ** 2 / distance if accelerate else 0
  print(accelerator)
  return (1 + accelerator) * (diff.xz - offset.xz)

def follow_behind(pos: glm.vec3, dest: glm.vec3, desDist: float, accelerate: bool) -> glm.vec3:
  diff = dest - pos
  if glm.length(diff) == desDist:
    return glm.vec3(0)
  offset = desDist * glm.normalize(diff)
  accelerator = (desDist - glm.length(diff)) ** 2 / glm.length(diff) if accelerate else 0
  return (1 + accelerator) * (diff - offset)

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
  catTex = SheetTexture("catGroove.bmp", (6, 7))
  fontTex = SheetTexture("font.bmp", (26, 3))

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

  animIndex = 0
  bbSquare = RenderObject.SquareBB(renderer)
  bbSquare.modelMat = glm.translate(bbSquare.modelMat, glm.vec3(0, 1, 0))
  bbSquare.texture = catTex
  renderManager.add_object(bbSquare)

  text = RenderObject.SquareUI(renderer)
  letters: list[RenderObject.SquareUI] = []
  letterIds = (64, 3, 0, 13, 6, 4, 17, 64)
  color = glm.vec4(1, 0, 0, 1)
  textTex = Texture(32 * len(letterIds), 32)
  text.texture = textTex
  textLayer = Layer(-1, False)
  textLayer.customProjection = glm.ortho(0, 32 * len(letterIds), 0, 32, -100, 100)
  for i in range(len(letterIds)):
    index = letterIds[i]
    letter = RenderObject.SquareUI(renderer)
    letters.append(letter)
    letter.modelMat = glm.translate(letter.modelMat, glm.vec3(16 + 32 * i, 16, 0))
    letter.modelMat = glm.scale(letter.modelMat, glm.vec3(32, 32, 1))
    letter.texture = fontTex
    letter.colorFilter = color
    letter.texOffsetScale = letter.texture.get_square(index)
    renderManager.add_object(letter, textLayer)
  renderManager.draw_layer_onto_texture(textLayer, text.texture)
  renderManager.add_object(text, 2)
  text.modelMat = glm.scale(glm.translate(text.modelMat, glm.vec3(400, 400, 0)), glm.vec3(32 * len(letterIds), 32, 1))

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
  renderer.set_uniform("texOffsetScale", glm.vec4(0.5, 0.5, 0.5, 0.5))

  renderer.swap_program("billboard")
  renderer.set_uniform("viewMat", viewMat)
  renderer.set_uniform("colorFilter", glm.vec4(1, 0, 1, 1))

  renderer.swap_program("ui")
  renderer.set_uniform("colorFilter", glm.vec4(1, 0, 1, 1))

  camPos = glm.vec3(0, 2.5, -3)
  camTarget = glm.vec3(0, 1.5, 0)
  playerPos = glm.vec3(0, 1, 0)

  glfw.show_window(renderer.window)

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
      camPos += speed * 2 * camRight
      camMoved = True
    if Input.is_held(glfw.KEY_E):
      camPos -= speed * 2 * camRight
      camMoved = True
    if Input.is_held(glfw.KEY_R):
      if camPos.y <= camTarget.y - 2.5:
        camPos.y = camTarget.y - 2.5
      else:
        camPos -= speed * 2 * camUp
    if Input.is_held(glfw.KEY_F):
      if camPos.y >= camTarget.y + 2.5:
        camPos.y = camTarget.y + 2.5
      else:
        camPos += speed * 2 * camUp

    if playerMovement != glm.vec2(0):
      playerPos.xz += speed * glm.normalize(playerMovement)
      if camMoved:
        camPos.xz += speed * glm.normalize(playerMovement)
    
    bbSquare.modelMat = glm.translate(glm.mat4(1), playerPos)
      
    camTarget += (delta * 20 if delta * 20 < 1 else 1) * follow_behind(camTarget, playerPos + glm.vec3(0, 0.5, 0), 0, False)
    camPos.xz += follow_behind_xz(camPos, camTarget, 3, True)
    
    for i in range(len(grapeOverlords)):
      grapeOverlord = grapeOverlords[i]
      grapeOverlord.colorFilter = glm.vec4(0.75 + glm.sin(glfw.get_time()) / 4, 0.75 + glm.cos(glfw.get_time()) / 4, 0.75 - glm.sin(glfw.get_time()) / 4, 1)
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
    
    animIndex += 20 * delta
    bbSquare.texOffsetScale = catTex.get_square(int(animIndex) % catTex.frameCount)

    text.colorFilter = glm.vec4(1, 1, 1, 0.5 + glm.sin(glfw.get_time() * 4) / 2)

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