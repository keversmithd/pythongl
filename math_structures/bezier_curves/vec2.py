import numpy as np
import math

def draw_rectangle(r):

    print ("\\draw (" +str(r[0])+"," +str(r[1]) + ") rectangle " + "(" + str(r[2]) + "," + str(r[3]) + ")")

def draw_point(p):

    print(f'\\draw ({p[0]}cm,{p[1]}cm) circle (2pt);')

def draw_line(o, v, t):
    print(f'\\draw ({o[0]}cm,{o[1]}cm) -- ({o[0] + v[0]*t}cm,{o[1] + v[1]*t}cm);')

class vec2:

    def __init__(self, x,y):

        self.p0 = x
        self.p1 = y

    def bounding_rectangle(self):

        minX = min(self.p0[0], self.p1[0])
        minY = min(self.p0[1], self.p1[1])

        maxX = max(self.p0[0], self.p1[0])
        maxY = max(self.p0[1], self.p1[1])

        return [minX, minY, maxX, maxY]

    def display(self):

        print(f'\\draw ({self.p0[0]}cm,{self.p0[1]}cm) -- ({self.p1[0]}cm,{self.p1[1]}cm);')

    def sample(self, t):
        
        v = [self.p1[0] - self.p0[0], self.p1[1] - self.p0[0]]
        v_norm = math.sqrt( v[0]*v[0] + v[1]*v[1] )
        v[0] /= v_norm
        v[1] /= v_norm
        return [self.p0[0] + v[0]*t, self.p0[1] + v[1]*t]

    def intersects_line(self, origin, vector):

        o = self.p0
        v = [self.p1[0]-self.p0[0], self.p1[1]-self.p0[1]]

        if ( v[0] == 0 ):
            print("intersects line zero vec2 zero")
            return None

        d = (vector[1] - ((v[1]*vector[0])/v[0]))

        if ( d == 0 ):
            print("desc zero zero")
            return None
        n = (o[1] + ((v[1]*origin[0])/(v[0])) - origin[1])/vector[1]

        t = n/d

        return self.sample(t)

    def project_onto(self, p):

        ax_x = self.p1[0] - self.p0[0]
        ax_y = self.p1[1] - self.p0[1]

        to_a_x = self.p0[0] - p[0]
        to_a_y = self.p0[1] - p[1]

        am = math.sqrt( ax_x*ax_x + ax_y*ax_y )
        
        if ( am == 0 ):
            print("project_onto: bad line")

        Vd = -(to_a_x*ax_x + to_a_y*ax_y)/(am*am)

        if ( Vd < 0 ):
            Vd = 0
        if ( Vd > 1 ):
            Vd = 1

        return np.array([ self.p0[0] + ax_x*Vd, self.p0[1] + ax_y*Vd ])

    def rough_normal(self):

        return  [self.p1[0], -self.p0[0]]

    def point_distance(self, closest_point, sample_point):

        projected = self.project_onto(closest_point)
    
        norm_distance = np.linalg.norm(np.subtract( projected, sample_point))
        a_distance = np.linalg.norm(np.subtract( self.p0, sample_point ))
        b_distance = np.linalg.norm(np.subtract( self.p1, sample_point))

        return min(norm_distance, a_distance, b_distance), projected
            

a = vec2([0,-0.5], [1,-1])

 

l = [[-1,-1], [1,1]]
draw_line(l[0],l[1], 1)
draw_line(a.p0, a.p1, 1)
point = a.intersects_line(l[0],l[1])
draw_point(point)