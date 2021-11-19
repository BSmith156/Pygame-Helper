import math

def get_pixel(pos, offset, zoom):
    return (math.floor((pos[0] / zoom) - (offset[0] / zoom)),
            math.floor((pos[1] / zoom) - (offset[1] / zoom)))