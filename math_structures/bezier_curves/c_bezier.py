import math

def draw_rectangle(r):

    print ("\\draw (" +str(r[0])+"," +str(r[1]) + ") rectangle " + "(" + str(r[2]) + "," + str(r[3]) + ")")

def draw_point(p):

    print("\\draw (" + str(p[0]) + "," + str(p[1]) + ")")

def quadratic_solution(a,b,c):

    if ( a == 0 ):
        return [0,0]


    t1 = -b + math.sqrt(math.pow(b,2) - 4*a*c)/(2*a)
    t2 = -b - math.sqrt(math.pow(b,2) + 4*a*c)/(2*a)

    return [t1,t2]


def solve_cubic(a,b,c,d):

    

    if ( a == 0 ):
        q_solution = quadratic_solution(b,c,d)

        return [q_solution[0], q_solution[1], 1]
    if ( d == 0 ):
        da = a
        db = b/a
        dc = c/a
        q_solution = quadratic_solution(db,dc, 0)

        return [-1, q_solution[0], q_solution[1]]
    
    b = b/a
    c = c/a
    d = d/a

    q = (3.0*c - (b*b))/9.0
    r = -(27.0*d) + b*(9.0*c - 2.0*(b*b))
    r = r/54.0
    disc = q*q*q + r*r

    term1 = (b/3.0)

    solution = [-1,-1,-1]

    if ( disc > 0 ):
        s = r + math.sqrt(disc)
        s = -math.pow(-s, (1.0/3.0)) if (s < 0) else math.pow(s, (1.0/3.0))
        t = r - math.sqrt(disc)
        t = -math.pow(-t, (1.0/3.0)) if (t < 0) else math.pow(t, (1.0/3.0))
        solution[0] = -term1 + s + t
        term1 += (s+t)/2.0
        solution[1] = -term1
        solution[2] = -term1
    
        return solution
    if ( disc == 0 ):

        r13 = math.pow(-r, (1.0/3.0)) if (r<0) else math.pow(r, (1.0/3.0))
        solution[0] = -term1 + 2.0*r13
        solution[1] = -(r13 + term1)
        solution[2] = -(r13 + term1)

        return solution

    q = -q
    dum1 = q*q*q
    dum1 = math.acos(r/math.sqrt(dum1))
    r13 = 2.0 * math.sqrt(q)
    solution[0] = -term1 + r13*cos(dum1/3.0)
    solution[1] = -term1 + r13*cos((dum1 + 2.0*math.pi)/3.0)
    solution[2] = -term1 + r13*cos((dum1 + 4.0*math.pi)/3.0)
    return solution


class c_bezier:

    def __init__(self, p0, p1, p2, p3):

        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def sample(self, t):
        x = math.pow((1-t),3)*self.p0[0] + 3*math.pow((1-t),2)*t*self.p1[0] + 3*(1-t)*math.pow(t,2)*self.p2[0] + math.pow(t,3)*self.p3[0]
        y = math.pow((1-t),3)*self.p0[1] + 3*math.pow((1-t),2)*t*self.p1[1] + 3*(1-t)*math.pow(t,2)*self.p2[1] + math.pow(t,3)*self.p3[1]
        
        return [x,y]

    def min_max(self):
        solution = [-1,-1,-1,-1]

        i = self.p1[0] - self.p0[0]
        j = self.p2[0] - self.p1[0]
        k = self.p3[0] - self.p2[0]

        a = (3*i - 6*j + 3*k)
        b = (6*j - 6*i)
        c = 3*i

        sqrtPart =  (b*b) - (4*a*c)
        hasSolution = (sqrtPart >= 0)
        if ( hasSolution == True):
            t1 = (-b + math.sqrt(sqrtPart))/(2*a)
            t2 = (-b - math.sqrt(sqrtPart))/(2*a)
            solution[0] = t1
            solution[1] = t2

        i = self.p1[1] - self.p0[1]
        j = self.p2[1] - self.p1[1]
        k = self.p3[1] - self.p2[1]

        a = (3*i - 6*j + 3*k)
        b = (6*j - 6*i)
        c = 3*i

        sqrtPart =  (b*b) - (4*a*c)
        hasSolution = (sqrtPart >= 0)
        if ( hasSolution == True ):
            t1 = (-b + math.sqrt(sqrtPart))/(2*a)
            t2 = (-b - math.sqrt(sqrtPart))/(2*a)
            solution[2] = t1
            solution[3] = t2

        return solution

    def bounding_rectangle(self):

        solution = self.min_max()

        minX = min(self.p0[0], self.p3[0])
        minY = min(self.p0[1], self.p3[1])

        maxX = max(self.p0[0], self.p3[0])
        maxY = max(self.p0[1], self.p3[1])

        for i in range(0, 4):
            if solution[i] != -1:

                sample_point = self.sample( solution[i] )

                minX = min(minX, sample_point[0])
                minY = min(minY, sample_point[1])

                maxX = max(maxX, sample_point[0])
                maxY = max(maxY, sample_point[1])

    def solve_by_point(self, point):

        solution = [-1,-1,-1,-1,-1,-1]

        c_x = solve_cubic(self.p0[0], self.p1[0], self.p2[0], self.p3[0])
        c_y = solve_cubic(self.p0[1], self.p1[1], self.p2[1], self.p3[1])

        sol_pointer = 0

        for i in range(0, 3):
            if ( c_x[i] != -1 and c_x[i] >= 0 and c_x[i] <= 1):
                solution[sol_pointer] = c_x[i]
                sol_pointer += 1

        for i in range(0, 3):
            if ( c_y[i] != -1 and c_y[i] >= 0 and c_y[i] <= 1):
                solution[sol_pointer] = c_y[i]
                sol_pointer += 1

        return solution

    def point_distance(self, point):

        solutions = self.solve_by_point(point)
        for i in range(0,6):
            l = 1+1
        return 0
        

        min_distance = 2139123
        min_point = 0

        for i in range(0, 6):

            if ( solutions[i] != -1 ):

                sample_point = self.sample( solutions[i] )
                length = math.sqrt( math.pow( (sample_point[0] - point[0]),2) + math.pow( (sample_point[1] - point[1]), 2) )

                if ( length < min_distance ):
                    min_distance = length
                    min_point = sample_point



q = c_bezier( [0.0, 0.0], [10.0, 11], [12,-12], [13,0] )
solution = q.min_max()

c_solution = solve_cubic(1.0, 2.0, 3.0, 4.0)




