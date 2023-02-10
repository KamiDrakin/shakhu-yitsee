import glm

from Texture import Texture

class AnimatedTexture(Texture):
  def __init__(self, name: str, sheetSize: tuple[int]):
    super().__init__(name)
    self.sheetWidth = sheetSize[0]
    self.frameCount = self.sheetWidth * sheetSize[1]
    self.sizeRatio = glm.vec2(1 / sheetSize[0], 1 / sheetSize[1])
  
  def get_square(self, index: int) -> glm.vec4:
    offsetIndex = glm.vec2(index % self.sheetWidth, int(index / self.sheetWidth))
    return glm.vec4(offsetIndex * self.sizeRatio, 1 / self.sizeRatio)