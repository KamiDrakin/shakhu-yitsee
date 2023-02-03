import glfw

class Input:
  window = None
  prevHeld: dict[int, bool] = {}
  held: dict[int, bool] = {}
  pressed: dict[int, bool] = {}
  released: dict[int, bool] = {}

  def init(window):
    Input.window = window
    glfw.set_key_callback(window, key_callback)

  def update():
    for key in Input.held:
      Input.released[key] = False
      Input.pressed[key] = False
      if key not in Input.prevHeld.keys():
        Input.prevHeld[key] = False
      if Input.held[key]:
        if not Input.prevHeld[key]:
          Input.pressed[key] = True
      elif Input.prevHeld[key]:
        Input.released[key] = True
    Input.prevHeld = Input.held.copy()
    
  def is_held(key: int) -> bool:
    if key not in Input.held.keys():
      return False
    return Input.held[key]

  def is_pressed(key: int) -> bool:
    if key not in Input.pressed.keys():
      return False
    return Input.pressed[key]

  def is_released(key: int) -> bool:
    if key not in Input.released.keys():
      return False
    return Input.released[key]

def key_callback(window, key: int, scancode: int, action: int, mods: int):
  if action == glfw.PRESS:
    Input.held[key] = True
  elif action == glfw.RELEASE:
    Input.held[key] = False
  
