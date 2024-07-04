import math
import numpy as np

def draw_rectangle(r):

    print ("\\draw (" +str(r[0])+"," +str(r[1]) + ") rectangle " + "(" + str(r[2]) + "," + str(r[3]) + ")")

def draw_point(p):

    print(f'\\draw ({p[0]}cm,{p[1]}cm) circle (2pt);')

def draw_line(o, v, t):
    print(f'\\draw ({o[0]}cm,{o[1]}cm) -- ({o[0] + v[0]*t}cm,{o[1] + v[1]*t}cm);')

class q_bezier:

    def __init__(self, p0, p1, p2):

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

    def sample(self, t):
        x = math.pow((1-t),2)*self.p0[0] + 2*(1-t)*t*self.p1[0] + math.pow(t,2)*self.p2[0]
        y = math.pow((1-t),2)*self.p0[1] + 2*(1-t)*t*self.p1[1] + math.pow(t,2)*self.p2[1]

        return [x,y]

    def bounding_rectangle(self):

        minX = min(self.p0[0], self.p2[0])
        minY = min(self.p0[1], self.p2[1])

        maxX = max(self.p0[0], self.p2[0])
        maxY = max(self.p0[1], self.p2[1])

        disc = (self.p0[0] - 2*self.p1[0] + self.p2[0])
        disc2 = (self.p0[1] - 2*self.p1[1] + self.p2[1])

        if ( disc != 0 ):
            t = (self.p0[0] - self.p1[0])/disc

            if ( t >= 0 and t <= 1):
                sample = self.sample(t)

                minX = min(minX, sample[0])
                minY = min(minY, sample[1])

                maxX = max(maxX, sample[0])
                maxY = max(maxY, sample[1])

        if ( disc2 != 0 ):
            t = (self.p0[1] - self.p1[1])/disc2

            if ( t >= 0 and t <= 1):
                sample = self.sample(t)

                minX = min(minX, sample[0])
                minY = min(minY, sample[1])

                maxX = max(maxX, sample[0])
                maxY = max(maxY, sample[1])

        return [minX, minY, maxX, maxY]

    def solve_by_point(self, point):
        p0 = self.p0
        p1 = self.p1
        p2 = self.p2

        boundary_epsilon = 0.005

        px, py = point

        solution = [-1, -1, -1, -1]

        # Solving for x-component
        a_x = p0[0] - 2 * p1[0] + p2[0]
        b_x = -2 * p0[0] + 2 * p1[0]
        c_x = p0[0] - px

        disc_x = b_x**2 - 4 * a_x * c_x

        if a_x == 0:  # Handle linear case
            if b_x != 0:
                t_x = -c_x / b_x
                if 0 <= t_x <= 1:
                    solution[0] = t_x
        else:
            if disc_x >= 0:
                t1_x = (-b_x + math.sqrt(disc_x)) / (2 * a_x)
                t2_x = (-b_x - math.sqrt(disc_x)) / (2 * a_x)

                if ( t1_x <= -boundary_epsilon ):
                    t1_x = 0.0
                if ( t2_x <= -boundary_epsilon ):
                    t2_x = 0.0
                if ( t1_x > 1.0 and t1_x <= 1+boundary_epsilon ):
                    t1_x = 0.0
                if ( t2_x > 1.0 and t2_x <= 1+boundary_epsilon ):
                    t2_x = 0.0

                if 0 <= t1_x <= 1:
                    solution[0] = t1_x
                if 0 <= t2_x <= 1:
                    solution[1] = t2_x

        # Solving for y-component
        a_y = p0[1] - 2 * p1[1] + p2[1]
        b_y = -2 * p0[1] + 2 * p1[1]
        c_y = p0[1] - py

        disc_y = b_y**2 - 4 * a_y * c_y

        if a_y == 0:  # Handle linear case
            if b_y != 0:
                t_y = -c_y / b_y
                if 0 <= t_y <= 1:
                    solution[2] = t_y
        else:
            if disc_y >= 0:
                t1_y = (-b_y + math.sqrt(disc_y)) / (2 * a_y)
                t2_y = (-b_y - math.sqrt(disc_y)) / (2 * a_y)

                if ( t1_y <= -boundary_epsilon ):
                    t1_y = 0.0
                if ( t2_y <= -boundary_epsilon ):
                    t2_y = 0.0
                if ( t1_y > 1.0 and t1_y <= 1+boundary_epsilon ):
                    t1_y = 0.0
                if ( t2_y > 1.0 and t2_y <= 1+boundary_epsilon ):
                    t2_y = 0.0

                if 0 <= t1_y <= 1:
                    solution[2] = t1_y
                if 0 <= t2_y <= 1:
                    solution[3] = t2_y

        return solution

    def rough_normal(self):
        return [self.p0[1], -self.p2[0]]

    def display(self):

        print(  f'\\draw ({self.p0[0]}cm, {self.p0[1]}cm) to[quadratic={{({self.p1[0]}cm, {self.p1[1]}cm)}}] ({self.p2[0]}cm, {self.p2[1]}cm);'  )

    def solve_quadratic(self, a, b, c):

        solutions = [-1, -1]

        disc = (b*b) - (4*a*c)
        boundary_epsilon = 0.005

        if a == 0:  # Handle linear case
            if b != 0:
                t = -c / b
                if 0 <= t <= 1:
                    solution[0] = t
        else:
            if disc >= 0:
                t1 = (-b + math.sqrt(disc)) / (2 * a)
                t2 = (-b - math.sqrt(disc)) / (2 * a)

                if ( t1 <= -boundary_epsilon ):
                    t1 = 0.0
                if ( t2 <= -boundary_epsilon ):
                    t2 = 0.0
                if ( t1 > 1.0 and t1 <= 1+boundary_epsilon ):
                    t1 = 0.0
                if ( t2 > 1.0 and t2 <= 1+boundary_epsilon ):
                    t2 = 0.0

                if 0 <= t1 <= 1:
                    solutions[0] = t1
                if 0 <= t2 <= 1:
                    solutions[1] = t2

        return solutions


    # given the origin of a line and the vector associated with the line find the intersection point between the two.
    def intersects_line(self, origin, vector):

        vector_norm = math.sqrt(vector[0]**2 + vector[1]**2)
        if ( vector_norm == 0 ):
            return None
        norm_vector = [vector[0]/vector_norm, vector[1]/vector_norm]

        a = (self.p0[1] - (self.p0[0]*vector[1])/vector[0]) - 2*(self.p1[1] - (self.p1[0]*vector[1])/vector[0]) + (self.p2[1] - (self.p2[0]*vector[1])/vector[0])
        b = -2*(self.p0[1] - (self.p0[0]*vector[1])/vector[0]) + 2*(self.p1[1] - (self.p1[0]*vector[1])/vector[0])
        c = (self.p0[1] - (self.p0[0]*vector[1])/vector[0]) + (origin[0]*vector[1] ) - (origin[1])

        solutions = self.solve_quadratic(a,b,c)

        # get the s value which is farthest away from zero or one while still being in the range 0 to 1
        closest_to_middle = 2
        # if s is the parameter of the current curve
        s = -1

        if ( solutions[0] >= 0 or solutions[0] <= 1 ):

            closest_to_middle = math.fabs(0.5 - solutions[0])
            s = solutions[0]
        if ( solutions[1] >= 0 or solutions[1] <= 1 ):

            middle_distance = math.fabs( 0.5 - solutions[1] )

            if ( middle_distance < closest_to_middle ):
                s = solutions[1]

        if ( s == -1 ):
            return None
        
        t = ((1-(s*s))*self.p0[0] + 2*(1-s)*s*self.p1[0] + (s*s)*self.p2[0] - origin[0])/vector[0]

        if ( t < 0 or t > 1 ):
            print("not on line!")

        return self.sample(s)




    def point_distance(self, closest_point, sample_point):

        p0 = self.p0
        p1 = self.p1
        p2 = self.p2

        curve_point = [0,0]
        min_point = [0,0]

        solution = self.solve_by_point(closest_point)

        min_distance = 1213891

        t = solution[0]
        if ( t != -1 ):
            curve_point[0] = math.pow((1-t),2)*p0[0] + 2*(1-t)*t*p1[0] + math.pow(t,2)*p2[0]
            curve_point[1] = math.pow((1-t),2)*p0[1] + 2*(1-t)*t*p1[1] + math.pow(t,2)*p2[1]

            directed_edge = [curve_point[0] - sample_point[0], curve_point[1] - sample_point[1] ]
            length = math.sqrt( math.pow( directed_edge[0], 2) + math.pow( directed_edge[1], 2) )

            if ( length < min_distance ):
                min_distance = length
                min_point[0] = curve_point[0]
                min_point[1] = curve_point[1]

        t = solution[1]
        if ( t != -1 ):
            curve_point[0] = math.pow((1-t),2)*p0[0] + 2*(1-t)*t*p1[0] + math.pow(t,2)*p2[0]
            curve_point[1] = math.pow((1-t),2)*p0[1] + 2*(1-t)*t*p1[1] + math.pow(t,2)*p2[1]

            directed_edge = [curve_point[0] - sample_point[0], curve_point[1] - sample_point[1] ]
            length = math.sqrt( math.pow( directed_edge[0], 2) + math.pow( directed_edge[1], 2) )

            if ( length < min_distance ):
                min_distance = length
                min_point[0] = curve_point[0]
                min_point[1] = curve_point[1]

        t = solution[2]
        if ( t != -1 ):
            curve_point[0] = math.pow((1-t),2)*p0[0] + 2*(1-t)*t*p1[0] + math.pow(t,2)*p2[0]
            curve_point[1] = math.pow((1-t),2)*p0[1] + 2*(1-t)*t*p1[1] + math.pow(t,2)*p2[1]

            directed_edge = [curve_point[0] - sample_point[0], curve_point[1] - sample_point[1] ]
            length = math.sqrt( math.pow( directed_edge[0], 2) + math.pow( directed_edge[1], 2) )

            if ( length < min_distance ):
                min_distance = length
                min_point[0] = curve_point[0]
                min_point[1] = curve_point[1]

        t = solution[3]
        if ( t != -1 ):
            curve_point[0] = math.pow((1-t),2)*p0[0] + 2*(1-t)*t*p1[0] + math.pow(t,2)*p2[0]
            curve_point[1] = math.pow((1-t),2)*p0[1] + 2*(1-t)*t*p1[1] + math.pow(t,2)*p2[1]

            directed_edge = [curve_point[0] - sample_point[0], curve_point[1] - sample_point[1] ]
            length = math.sqrt( math.pow( directed_edge[0], 2) + math.pow( directed_edge[1], 2) )

            if ( length < min_distance ):
                min_distance = length
                min_point[0] = curve_point[0]
                min_point[1] = curve_point[1]

        l0 = np.linalg.norm( np.array(p0) - np.array(sample_point) )

        if (  l0 < min_distance ):
            min_distance = l0
            min_point[0] = p0[0]
            min_point[1] = p0[1]

        l2 = np.linalg.norm( np.array(p2) - np.array(sample_point) )

        if (  l2 < min_distance ):
            min_distance = l2
            min_point[0] = p2[0]
            min_point[1] = p2[1]

        # calculate in or out status
        

        return min_distance, min_point
                

# mode = q_bezier([0,0], [0.5, 0.5], [1.5, -2.0])

# draw_line([0,-2], [1,2], 2)

# point = mode.line_intersection([0,-2],  [1,2])

# draw_point(point)
# mode.display()