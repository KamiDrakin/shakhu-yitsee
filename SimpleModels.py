def shift_center(model: list[float], stride: int, shift: tuple[float]) -> list[float]:
  model = model.copy()
  for i in range(len(model)):
    if i % stride < 3:
      model[i] += shift[i % stride]
    i += 1
  return model

cubeFull = [
  -0.5, -0.5, -0.5,  0.0, 0.0, 0.0,
   0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
   0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
   0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
  -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,
  -0.5, -0.5, -0.5,  0.0, 0.0, 0.0,

  -0.5, -0.5,  0.5,  0.0, 0.0, 0.0,
   0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
   0.5,  0.5,  0.5,  1.0, 1.0, 0.0,
   0.5,  0.5,  0.5,  1.0, 1.0, 0.0,
  -0.5,  0.5,  0.5,  0.0, 1.0, 0.0,
  -0.5, -0.5,  0.5,  0.0, 0.0, 0.0,

  -0.5,  0.5,  0.5,  1.0, 0.0, 0.0,
  -0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
  -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
  -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
  -0.5, -0.5,  0.5,  0.0, 0.0, 0.0,
  -0.5,  0.5,  0.5,  1.0, 0.0, 0.0,

   0.5,  0.5,  0.5,  1.0, 0.0, 0.0,
   0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
   0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
   0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
   0.5, -0.5,  0.5,  0.0, 0.0, 0.0,
   0.5,  0.5,  0.5,  1.0, 0.0, 0.0,

  -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
   0.5, -0.5, -0.5,  1.0, 1.0, 0.0,
   0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
   0.5, -0.5,  0.5,  1.0, 0.0, 0.0,
  -0.5, -0.5,  0.5,  0.0, 0.0, 0.0,
  -0.5, -0.5, -0.5,  0.0, 1.0, 0.0,

  -0.5,  0.5, -0.5,  0.0, 1.0, 0.0,
   0.5,  0.5, -0.5,  1.0, 1.0, 0.0,
   0.5,  0.5,  0.5,  1.0, 0.0, 0.0,
   0.5,  0.5,  0.5,  1.0, 0.0, 0.0,
  -0.5,  0.5,  0.5,  0.0, 0.0, 0.0,
  -0.5,  0.5, -0.5,  0.0, 1.0, 0.0
]

squareFull = [
  -0.5, -0.5, 0.0,  0.0, 0.0, 0.0,
   0.5, -0.5, 0.0,  1.0, 0.0, 0.0,
   0.5,  0.5, 0.0,  1.0, 1.0, 0.0,
   0.5,  0.5, 0.0,  1.0, 1.0, 0.0,
  -0.5,  0.5, 0.0,  0.0, 1.0, 0.0,
  -0.5, -0.5, 0.0,  0.0, 0.0, 0.0
]

triangleFull = [
  -0.5, -0.5, 0.0, 0.0,
   0.5, -0.5, 0.0, 0.0,
   0.0,  0.5, 0.0, 0.0
]