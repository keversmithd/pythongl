import math
import numpy as np

#returns the np array of the point projected onto the line
def project_onto(p, a, b):

    ax_x = b[0] - a[0]
    ax_y = b[1] - a[1]

    to_a_x = a[0] - p[0]
    to_a_y = a[1] - p[1]

    am = math.sqrt( ax_x*ax_x + ax_y*ax_y )
    
    if ( am == 0 ):
        print("project_onto: bad line")

    Vd = -(to_a_x*ax_x + to_a_y*ax_y)/(am*am)

    if ( Vd < 0 ):
        Vd = 0
    if ( Vd > 1 ):
        Vd = 1

    return np.array([a[0] + ax_x*Vd, a[1] + ax_y*Vd ])

def draw_point(p):
    print(f'\\draw ({p[0]}cm,{p[1]}cm) circle (1pt);')

def draw_rectangle(r):
    print (f'\\draw ({r[0]}cm, {r[1]}pt) rectangle ({r[2]}cm, {r[3]}cm);')

class sdf_grid_node:

    def __init__(self, container, value):
        self.container = container
        self.value = value
        return

class sdf_grid_value:

    def __init__(self, value):
        self.value = value
        return

    def point_distance(self, point):
        return math.pow( (self.value[0]-point[0]),2 ) + math.pow( (self.value[1]-point[1]),2)

class sdf_grid:

    # prefered container to have even dimensions and an even resolution
    def __init__(self, container, resolution ):

        self.container = container
        self.resolution = resolution

        # resolution is even and square along the container.

        self.grid = None
        self.generate_grid()
        
    def generate_grid(self):

        container_width = self.container[2] - self.container[0]
        container_height = self.container[3] - self.container[1]

        # size of a single cell in the x direction
        self.x_length = container_width/self.resolution
        # size of a single cell in the y direction
        self.y_length = container_height/self.resolution

        self.grid = [[] for _ in range(0, self.resolution*self.resolution)]

    def cell_index(self, x,y):
        grid_origin = [ self.container[0], self.container[1] ]
        
        x_diff = x-grid_origin[0]
        y_diff = y-grid_origin[1]

        x_cell = math.floor( x_diff/self.x_length )
        y_cell = math.floor( y_diff/self.y_length )

        if ( x_cell == self.resolution ):
            x_cell = self.resolution-1
        if ( y_cell == self.resolution ):
            y_cell = self.resolution-1

        return math.floor ( (y_cell*self.resolution) + x_cell )

    def cell_row(self, x, y):

        grid_origin = [ self.container[0], self.container[1] ]
        
        x_diff = x-grid_origin[0]
        y_diff = y-grid_origin[1]

        x_cell = math.floor( x_diff/self.x_length )
        y_cell = math.floor ( y_diff/self.y_length )

        if ( y_cell == self.resolution ):
            return self.resolution-1

        return y_cell

    def cell_column(self, x,y):
        grid_origin = [ self.container[0], self.container[1] ]
        
        x_diff = x-grid_origin[0]
        y_diff = y-grid_origin[1]

        x_cell = math.floor( x_diff/self.x_length )

        return x_cell

    def insert_container(self, container, value):

        container_width = container[2] - container[0]
        container_height = container[3] - container[1]

        if ( container_height == 0 ):
            parent_container_height = (self.container[3]-self.container[1])
            
            container[1] -= parent_container_height*0.3
            container[3] += parent_container_height*0.3

            if ( container[1] < self.container[0]):
                container[1] = self.container[1]
            if ( container[3] > self.container[3]):
                container[3] = self.container[3]

        # possibly add one if x_steps is zero and container width is greater than zero 
        x_steps = math.floor(container_width/self.x_length)+1
        x_remainder = math.modf(container_width/self.x_length)[0]
        y_steps = math.floor(container_height/self.y_length)+1
        y_remainder = math.modf(container_height/self.y_length)[0]

        origin = [container[0], container[1]]

        new_node = sdf_grid_node(container, value)

        inserted = {}

        for j in range(0, y_steps):
            for i in range(0, x_steps):

                # query point inside of the container
                query_point_x = container[0] + i*self.x_length
                query_point_y = container[1] + j*self.y_length

                cell_index = self.cell_index(query_point_x, query_point_y)

                if ( cell_index < len(self.grid) and cell_index not in inserted):
                    inserted[cell_index] = 1
                    self.grid[cell_index].append(new_node)

                if ( x_remainder > 0 and i == x_steps-1 ):
                    query_point_x = container[0] + i*self.x_length + x_remainder*self.x_length
                    query_point_y = container[1] + j*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)

                    if ( cell_index < len(self.grid) and cell_index not in inserted):
                        inserted[cell_index] = 1
                        self.grid[cell_index].append(new_node)

                if ( y_remainder > 0 and j == y_steps-1 ):
                    query_point_x = container[0] + i*self.x_length 
                    query_point_y = container[1] + j*self.y_length + y_remainder*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)

                    if ( cell_index < len(self.grid) and cell_index not in inserted):
                        inserted[cell_index] = 1
                        self.grid[cell_index].append(new_node)

                if ( x_remainder > 0 and y_remainder > 0 and j == y_steps-1 and i == x_steps-1 ):
                    query_point_x = container[0] + i*self.x_length + x_remainder*self.y_length
                    query_point_y = container[1] + j*self.y_length + y_remainder*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)
                    if ( cell_index < len(self.grid) and cell_index not in inserted ):
                        inserted[cell_index] = 1
                        self.grid[cell_index].append(new_node)

    def query_closest_cell(self, x, y):

    
        # number of pixels in each left right up and down for the container search.
        initial_dimensions = 2*self.x_length

        expansion_positive_x = x+initial_dimensions 
        expansion_negative_x = x-initial_dimensions

        expansion_positive_y = y+initial_dimensions
        expansion_negative_y = y-initial_dimensions

        # build the inital expansions
        if ( expansion_positive_x > self.container[2] ):
            expansion_positive_x = self.container[2] 
        if ( expansion_negative_x < self.container[0] ):
            expansion_negative_x = self.container[0]
        if ( expansion_positive_y > self.container[3] ):
            expansion_positive_y = self.container[3] 
        if ( expansion_negative_y < self.container[1] ):
            expansion_negative_y = self.container[1]

        minimum_id = [1000, 0]

        # do an inital proxy check of the container a,b,c,d for some inital miracle collision
        self.query_closest_simple_container(minimum_id, [expansion_negative_x,expansion_negative_y,expansion_positive_x,expansion_positive_y], (x,y))
        
        if ( minimum_id[0] == 1000 ):
            return 0.0, False

        return minimum_id[0], self.inside(x,y)

        #build the inital box at this scale.
        a = [ expansion_negative_x, expansion_negative_y ]
        b = [ expansion_positive_x, expansion_negative_y ]
        c = [ expansion_positive_x, expansion_positive_y ]
        d = [ expansion_negative_x, expansion_positive_y ]

        # set scale factor for how fast the rectangle grows
        scale_factor = 1.1

        # while nothing has been found in the area, then keep on searching and progressing.
        while ( minimum_id[1] == 0 ):

            expansion_width = (b[0] - a[0])
            expansion_height = (c[1] - b[1])

            # define set of scaled coordinates
            expansion_positive_x = c[0] + np.abs(scale_factor*expansion_width )
            expansion_positive_y = c[1] + np.abs(scale_factor*expansion_height )

            expansion_negative_x = a[0] - np.abs(scale_factor*expansion_width)
            expansion_negative_y = a[1] - np.abs(scale_factor*expansion_height)
            
            # respect of the limits of the container
            if ( expansion_positive_x > self.container[2] ):
                expansion_positive_x = self.container[2] 
                minimum_id[1] = 1.0
                break
            if ( expansion_negative_x < self.container[0] ):
                expansion_negative_x = self.container[0]
                minimum_id[1] = 1.0
                break
            if ( expansion_positive_y > self.container[3] ):
                expansion_positive_y = self.container[3]
                minimum_id[1] = 1.0 
                break
            if ( expansion_negative_y < self.container[1] ):
                expansion_negative_y = self.container[1]
                minimum_id[1] = 1.0
                break

            # define four rectangles to search based on a,b,c and d
            r0 = [ expansion_negative_x, c[1], expansion_positive_x, expansion_positive_y ]
            r1 = [ expansion_negative_x, a[1], a[0], c[1]  ]
            r2 = [ b[0], b[1], expansion_positive_x, c[1] ]
            r3 = [ expansion_negative_x, expansion_negative_y, expansion_positive_x, a[1]]

            # then test each rectangle
            self.query_closest_simple_container(minimum_id, r0, (x,y))
            self.query_closest_simple_container(minimum_id, r1, (x,y))
            self.query_closest_simple_container(minimum_id, r2, (x,y))
            self.query_closest_simple_container(minimum_id, r3, (x,y))

            # then set a,b,c,d to the respective limits
            a = [ expansion_negative_x, expansion_negative_y ]
            b = [ expansion_positive_x, expansion_negative_y ]
            c = [ expansion_positive_x, expansion_positive_y ]
            d = [ expansion_negative_x, expansion_positive_y ]

        return minimum_id[0]

    def inside(self, x,y):
        
        advance_right = self.container[2]-x
        advance_left = x-self.container[0]

        right_steps = math.floor(advance_right/self.x_length)
        right_remainder = math.modf(advance_right/self.x_length)
        left_steps = math.floor(advance_left/self.x_length)
        left_remainder = math.modf(advance_left/self.y_length)

        # imaginary horizontal line
        line_origin = [self.container[0], y]
        line_vector = [1,0]

        # count intersections
        intersections = 0

        previously_intersected = {}

        for r in range(0, right_steps):

            query_point_x = x + r*self.x_length
            query_point_y = y

            cell_index = self.cell_index(x,y)

            for j in range(0, len(self.grid[cell_index])):
                if ( self.grid[cell_index][j].value.intersects_line(line_origin, line_vector) == True and f'{cell_index},{j}' not in previously_intersected ):
                    previously_intersected[f'{cell_index},{j}'] = 1
                    intersections += 1


        return (intersections % 2 == 1 )

        
    # returns vector to minimum point from the point itself
    def directed_minimum_vector(self, cell_index, point):
        # open the grid cell
        grid_cell = self.grid[cell_index]
        for i in range(0, len(grid_cell)):

            # get the inner node
            node = grid_cell[i]
            # get the inner container
            container = node.container

            #draw_rectangle(container)

            # project this point onto the container
            proj0 = project_onto(point, [container[0], container[1]], [container[2], container[1]] )
            proj1 = project_onto(point, [container[2], container[1]], [container[2], container[3]] )
            proj2 = project_onto(point, [container[0], container[3]], [container[2], container[3]] )
            proj3 = project_onto(point, [container[0], container[1]], [container[1], container[3]] )
            point_p = np.array(point)

            # draw_point(proj0)
            # draw_point(proj1)
            # draw_point(proj2)
            # draw_point(proj3)

            norm0 = np.linalg.norm(  np.subtract(proj0, point_p)  )
            norm1 = np.linalg.norm ( np.subtract(proj1, point_p ) )
            norm2 = np.linalg.norm ( np.subtract(proj2, point_p ) )
            norm3 = np.linalg.norm ( np.subtract(proj3, point_p ) )

            closest_point = point
            closest_distance = 0

            if ( norm0 < norm1 ):
                closest_point = proj0
                closest_distance = norm0
            else:
                closest_point = proj1
                closest_distance = norm1

            if ( norm2 < closest_distance ):
                closest_distance = norm2
                closest_point = proj2

            if ( norm3 < closest_distance ):
                closest_distance = norm3
                closest_point = proj3
            

            distance, min_point = node.value.point_distance( closest_point, point )

            return [ min_point[0] - point[0], min_point[1] - point[1] ]

    # updates minimum_id with minimum distance among the items in the grid, and the node which point distance was the closest. 
    # minimum_id [min_distance, returned object.]
    def update_minimum_distance(self, minimum_id, cell_index, point):
        # open the grid cell
        grid_cell = self.grid[cell_index]
        distance = minimum_id[0]

        for i in range(0, len(grid_cell)):

            # get the inner node
            node = grid_cell[i]
            # get the inner container of the item in the node.
            container = node.container

            #draw_rectangle(container)

            # project this point onto the container
            proj0 = project_onto(point, [container[0], container[1]], [container[2], container[1]] )
            proj1 = project_onto(point, [container[2], container[1]], [container[2], container[3]] )
            proj2 = project_onto(point, [container[0], container[3]], [container[2], container[3]] )
            proj3 = project_onto(point, [container[0], container[1]], [container[0], container[3]] )

            point_p = np.array(point)

            # draw_point(proj0)
            # draw_point(proj1)
            # draw_point(proj2)
            # draw_point(proj3)

            norm0 = np.linalg.norm(  np.subtract(proj0, point_p)  )
            norm1 = np.linalg.norm ( np.subtract(proj1, point_p ) )
            norm2 = np.linalg.norm ( np.subtract(proj2, point_p ) )
            norm3 = np.linalg.norm ( np.subtract(proj3, point_p ) )

            closest_point = point
            closest_distance = 0

            if ( norm0 < norm1 ):
                closest_point = proj0
                closest_distance = norm0
            else:
                closest_point = proj1
                closest_distance = norm1

            if ( norm2 < closest_distance ):
                closest_distance = norm2
                closest_point = proj2

            if ( norm3 < closest_distance ):
                closest_distance = norm3
                closest_point = proj3
            
            #draw_point(closest_point)


            #node.value.display()
            distance, min_point = node.value.point_distance( closest_point, point )

            # if ( distance <= 1):
            #     draw_point(min_point)

            if ( distance < minimum_id[0] ):
                minimum_id[0] = distance
                minimum_id[1] = node

    # point is referenced against the distance between objects in the grid.
    def query_closest_simple_container(self, minimum_id, container, point):

        container_width = container[2] - container[0]
        container_height = container[3] - container[1]

        x_steps = math.floor(container_width/self.x_length)+1
        x_remainder = math.modf(container_width/self.x_length)[0]
        y_steps = math.floor(container_height/self.y_length)+1
        y_remainder = math.modf(container_height/self.y_length)[0]

        for j in range(0, y_steps):
            for i in range(0, x_steps):

                # query point inside of the container
                query_point_x = container[0] + i*self.x_length
                query_point_y = container[1] + j*self.y_length

                cell_index = self.cell_index(query_point_x, query_point_y)
                
                if ( cell_index > len(self.grid)-1):
                    print("ahhh")

                #updat the minimum distance
                self.update_minimum_distance(minimum_id, cell_index, point)
                
                if ( x_remainder > 0 and i == x_steps-1 ):
                    query_point_x = container[0] + i*self.x_length + x_remainder*self.x_length
                    query_point_y = container[1] + j*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)

                    if ( cell_index > len(self.grid)-1):
                        print("ahhh")

                    #update the minimum distance
                    self.update_minimum_distance(minimum_id, cell_index, point)


                if ( y_remainder > 0 and j == y_steps-1 ):
                    query_point_x = container[0] + i*self.x_length 
                    query_point_y = container[1] + j*self.y_length + y_remainder*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)

                    if ( cell_index > len(self.grid)-1):
                        print("ahhh")

                    #update the minimum distance
                    self.update_minimum_distance(minimum_id, cell_index, point)


                if ( x_remainder > 0 and y_remainder > 0 and j == y_steps-1 and i == x_steps-1 ):
                    query_point_x = container[0] + i*self.x_length + x_remainder*self.y_length
                    query_point_y = container[1] + j*self.y_length + y_remainder*self.y_length

                    cell_index = self.cell_index(query_point_x, query_point_y)

                    if ( cell_index > len(self.grid)-1):
                        print("ahhh")

                    #update the minimum distance
                    self.update_minimum_distance(minimum_id, cell_index, point)

        return minimum_id

