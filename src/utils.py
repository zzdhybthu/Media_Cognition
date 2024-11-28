from constants import *

def Cmp(pos, target):
    assert len(pos) == 3 and len(target) == 3, "Invalid position or target"
    delta = sum([(pos[i] - target[i]) ** 2 for i in range(3)]) ** 0.5
    print(f"cmp {pos=}, {target=}, {delta=}")
    return delta

def Pixel2Coord(pixel_x, pixel_y):
    x = BORDER_TOP - pixel_y * (BORDER_TOP - BORDER_BOTTOM)
    y = BORDER_LEFT - pixel_x * (BORDER_LEFT - BORDER_RIGHT)
    return x, y