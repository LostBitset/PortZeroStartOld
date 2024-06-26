# PortZero by HktOverload

import itertools, random
from utils import *

Export(...) @ globals()

class Coord2(t.NamedTuple):
    x: float; y: float

    def __add__(self, other):
        if not isinstance(other, Coord2):
            return NotImplemented
        return Coord2(
            x = self.x + other.x,
            y = self.y + other.y,
        )

    def __rmul__(self, other):
        if not isinstance(other, float):
            return NotImplemented
        return Coord2(
            x = self.x * other,
            y = self.y * other,
        )
    
    def __matmul__(self, other):
        if not isinstance(other, Coord3):
            return NotImplemented
        return ( 0.0
            + (self.x * other.x)
            + (self.y * other.y)
        )
    
    def __eq__(self, other):
        if not isinstance(other, Coord2):
            return NotImplemented
        return (
                almostEqual(self.x, other.x)
            and almostEqual(self.y, other.y)
        )

class Coord3(t.NamedTuple):
    x: float; y: float; z: float

    def __add__(self, other):
        if not isinstance(other, Coord3):
            return NotImplemented
        return Coord3(
            x = self.x + other.x,
            y = self.y + other.y,
            z = self.z + other.z,
        )

    def __rmul__(self, other):
        if not isinstance(other, float):
            return NotImplemented
        return Coord3(
            x = self.x * other,
            y = self.y * other,
            z = self.z * other,
        )

    def __matmul__(self, other):
        if not isinstance(other, Coord3):
            return NotImplemented
        return ( 0.0
            + (self.x * other.x)
            + (self.y * other.y)
            + (self.z * other.z)
        )

    def __eq__(self, other):
        if not isinstance(other, Coord3):
            return NotImplemented
        return (
                almostEqual(self.x, other.x)
            and almostEqual(self.y, other.y)
            and almostEqual(self.z, other.z)
        )

    def dropTo2(self) -> Coord2:
        return Coord2(x=self.x, y=self.y)

    def toH(self):
        return Coord3H(
            x=self.x,
            y=self.y,
            z=self.z,
            w = 1,
        )

class Tri2(t.NamedTuple):
    a: Coord2; b: Coord2; c: Coord2

    def mapVerts(self, fn: t.Callable[[Coord2], Coord2]):
        return Tri2(
            a = fn(self.a),
            b = fn(self.b),
            c = fn(self.c),
        )
    
    def __eq__(self, other):
        if not isinstance(other, Tri2):
            return NotImplemented
        return (
                self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )

class Tri3(t.NamedTuple):
    a: Coord3; b: Coord3; c: Coord3

    def mapVerts(self, fn: t.Callable[[Coord3], Coord3]):
        return Tri3(
            a = fn(self.a),
            b = fn(self.b),
            c = fn(self.c),
        )
    
    def mapTo2(self, fn: t.Callable[[Coord3], Coord2]):
        return Tri2(
            a = fn(self.a),
            b = fn(self.b),
            c = fn(self.c),
        )

    def dropTo2(self):
        return self.mapTo2(lambda x: x.dropTo2())
    
    def __eq__(self, other):
        if not isinstance(other, Tri3):
            return NotImplemented
        return (
                self.a == other.a
            and self.b == other.b
            and self.c == other.c
        )

class Hull(t.NamedTuple):
    verts: t.List[float]
    tris: t.List[Tri3]

class AABox(t.NamedTuple):
    c1: Coord3; c2: Coord3

    def promoteToHull(self) -> Hull:
        ...

Geometry = t.List[t.Union[Hull, AABox]]

def fastAABoxIntersection(a: AABox, b: AABox) -> bool:
    raise NotImplementedError

def gjkIntersection(a: Hull, b: Hull) -> bool:
    raise NotImplementedError

def intersects1(a, b):
    if isinstance(a, AABox) and isinstance(b, AABox):
        return fastAABoxIntersection(a, b)
    elif isinstance(a, AABox):
        return gjkIntersection(a.promoteToHull(), b)
    elif isinstance(b, AABox):
        return gjkIntersection(a, b.promoteToHull())
    else:
        return gjkIntersection(a, b)

def intersects(a: Geometry, b: Geometry) -> bool:
    for aSub, bSub in itertools.product(a, b):
        if intersects1(aSub, bSub):
            return False
    return True

def trisOfSub(sub: t.Union[Hull, AABox]):
    if isinstance(sub, Hull):
        return sub.tris
    else:
        return sub.promoteToHull().tris

def tris(geometry: Geometry) -> list[Tri3]:
    return [ i for sub in geometry for i in trisOfSub(sub) ]

class Coord3H(t.NamedTuple):
    x: float; y: float; z: float; w: float

    def __add__(self, other):
        if not isinstance(other, Coord3H):
            return NotImplemented
        return Coord3H(
            x = self.x + other.x,
            y = self.y + other.y,
            z = self.z + other.z,
            w = self.w + other.w,
        )

    def __rmul__(self, other):
        if not isinstance(other, float):
            return NotImplemented
        return Coord3H(
            x = self.x * other,
            y = self.y * other,
            z = self.z * other,
            w = self.w * other,
        )
    
    def __matmul__(self, other):
        if not isinstance(other, Coord3H):
            return NotImplemented
        return ( 0.0
            + (self.x * other.x)
            + (self.y * other.y)
            + (self.z * other.z)
            + (self.w * other.w)
        )
    
    def __eq__(self, other):
        if not isinstance(other, Coord3H):
            return NotImplemented
        return (
                almostEqual(self.x, other.x)
            and almostEqual(self.y, other.y)
            and almostEqual(self.z, other.z)
            and almostEqual(self.w, other.w)
        )

    @staticmethod
    def rand():
        return Coord3H(
            (random.random() - 0.5) * 2000,
            (random.random() - 0.5) * 2000,
            (random.random() - 0.5) * 2000,
            (random.random() - 0.5) * 2000,
        )
    
    def pd(self):
        return Coord3(
            x = self.x / self.w,
            y = self.y / self.w,
            z = self.z / self.w,
        )

class Xform3(t.NamedTuple):
    a: Coord3H; b: Coord3H; c: Coord3H; d: Coord3H
    # Columns

    def applyH(self, c: Coord3H):
        m = self
        return (
              (c.x * m.a)
            + (c.y * m.b)
            + (c.z * m.c)
            + (c.w * m.d)
        )
    
    def apply(self, c: Coord3):
        return self.applyH(
            c.toH()
        ).pd()
    
    def t(self):
        m = self
        return Xform3(
            Coord3H(m.a.x, m.b.x, m.c.x, m.d.x),
            Coord3H(m.a.y, m.b.y, m.c.y, m.d.y),
            Coord3H(m.a.z, m.b.z, m.c.z, m.d.z),
            Coord3H(m.a.w, m.b.w, m.c.w, m.d.w),
        )

    def __matmul__(self, other):
        if not isinstance(other, Xform3):
            return NotImplemented
        r, s = self, other.t()
        return Xform3(
            Coord3H(r.a@s.a, r.a@s.b, r.a@s.c, r.a@s.d),
            Coord3H(r.b@s.a, r.b@s.b, r.b@s.c, r.b@s.d),
            Coord3H(r.c@s.a, r.c@s.b, r.c@s.c, r.c@s.d),
            Coord3H(r.d@s.a, r.d@s.b, r.d@s.c, r.d@s.d),
        )
    
    def __eq__(self, other):
        if not isinstance(other, Xform3):
            return NotImplemented
        return (
                self.a == other.a
            and self.b == other.b
            and self.c == other.c
            and self.d == other.d
        )
    
    @staticmethod
    def rand():
        return Xform3(
            Coord3H.rand(),
            Coord3H.rand(),
            Coord3H.rand(),
            Coord3H.rand(),
        )
