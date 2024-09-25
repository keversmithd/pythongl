from sympy import Symbol
from sympy.matices import Matrix

x,y,z,cx,cy,cz,sx,sy,sz = Symbol('x y z cx cy cz sx sy sz')

Rx = Matrix([[1,0,0], [0,cx,-sy], [0,sy,cx]])
Ry = Matrix([[cx,-sy,0], [0,1,0], [0,sy,cx]])
Rz = Matrix([[cx, -sy, 0],[sy, cx, 0], [0,0,1]])

Rxyz = Rx*Ry*Rz

print ( Rxyz )