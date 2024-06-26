# PortZero by HktOverload

from utils import *
from geom import *

Export('Viewport') @ globals()

class Viewport(object):
    __slots__ = 'focalLength', 'xform'
    def __init__(self, focalLength: float, xform: Xform3):
        self.focalLength = focalLength
        self.xform = xform
    
    def project(self, vert: Coord3) -> Coord2:
        v = self.xform.apply(vert)
        if v.z <= 0:
            return None
        fac = self.focalLength / v.z
        return fac * v.dropTo2()
    
    def projectTri(self, tri: Tri3) -> Tri2:
        return tri.mapTo2(self.map)
