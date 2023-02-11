import glm

from Texture import Texture

class SheetTexture(Texture):
  def __init__(self, name: str, sheetSize: tuple[int]):
    super().__init__(name)
    self.sheetSize = sheetSize
    self.frameCount = sheetSize[0] * sheetSize[1]
    self.sizeRatio = glm.vec2(1 / sheetSize[0], 1 / sheetSize[1])
  
  def get_square(self, index: int) -> glm.vec4:
    offsetIndex = glm.vec2(index % self.sheetSize[0], self.sheetSize[1] - 1 - glm.floor(index / self.sheetSize[0]))
    return glm.vec4(offsetIndex * self.sizeRatio, 1 / self.sizeRatio)