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
        return np.array([a[0] , a[1]  ])

    Vd = -(to_a_x*ax_x + to_a_y*ax_y)/(am*am)

    if ( Vd < 0 ):
        Vd = 0
    if ( Vd > 1 ):
        Vd = 1

    return np.array([a[0] + ax_x*Vd, a[1] + ax_y*Vd ])


class sdf_quadnode:

    def __init__(self):
        
        self.leaf = False
        self.values = []
        self.children = []
        self.container = [0,0,0,0]
        self.value = None
        

    def init_node(self,container, value):
        self.container[0] = container[0]
        self.container[1] = container[1]
        self.container[2] = container[2]
        self.container[3] = container[3]

        self.value = copy.deepcopy(value)
    
    def init_leaf_node(self,container):
        self.container[0] = container[0]
        self.container[1] = container[1]
        self.container[2] = container[2]
        self.container[3] = container[3]
        self.leaf = True

    def init_non_leaf(self, container):
        self.container[0] = container[0]
        self.container[1] = container[1]
        self.container[2] = container[2]
        self.container[3] = container[3]
        self.leaf = False

    def add_value(self, value):
        self.value = value

def container_intersect(containerA, containerB):

    x_int = (containerA[0] >= containerB[0] and containerA[0] <= containerB[2]) or (containerA[0] <= containerB[0] and containerA[2] >= containerB[0])
    y_int = (containerA[1] >= containerB[1] and containerA[1] <= containerB[3]) or (containerA[1] <= containerB[1] and containerA[3] >= containerB[1])

    return x_int and y_int

def container_area(containerA):

    return (containerA[2]-containerA[0])*(containerA[3]-containerA[1])

class sdf_quadtree:

    def __init__( self, parent_container ):
        self.root = sdf_quadnode()
        self.root.init_leaf_node(parent_container)
    
        self.parent_container = parent_container
        self.maximum_area = container_area(parent_container)
        self.max_size = 5

    def insert( self, container, value ):

        current_node = sdf_quadnode()
        current_node.init_leaf_node(container)
        current_node.add_value(value)

        if ( container_intersect( container, self.parent_container ) ):
            self.insert_on_node(current_node, self.root)
        else:
            return
    
    def split_region_into_children(self, node):

        container = node.container

        container_width = container[2] - container[0]
        half_width = container_width/2
        container_height = container[3] - container[1]
        half_height = container_height/2

        lower_left_node = sdf_quadnode( )
        lower_left_node.init_leaf_node( [ container[0], container[1], container[0] +  half_width, container[1] + half_height] )
        lower_right_node = sdf_quadnode(  )
        lower_right_node.init_leaf_node( [ container[0]+half_width, container[1], container[0] + container_width, container[1] + half_height] )
        top_right_node = sdf_quadnode(  )
        top_right_node.init_leaf_node( [ container[0]+half_width, container[1]+half_height, container[0] + container_width, container[1] + container_height] )
        top_left_node = sdf_quadnode()
        top_left_node.init_leaf_node(  [ container[0], container[1]+half_height, container[0] + half_width, container[1] + container_height] )

        self.maximum_area = max(container_area(lower_right_node.container), container_area(lower_left_node.container))
        self.maximum_area = max(self.maximum_area, container_area(top_right_node.container))
        self.maximum_area = max(self.maximum_area, container_area(top_left_node.container))

        node.children.append(lower_left_node)
        node.children.append(lower_right_node)
        node.children.append(top_right_node)
        node.children.append(top_left_node)

    def redistribute(self,node):
        
        node.leaf = False
        
        self.split_region_into_children(node)

        for c in range(0, len(node.values)):
            self.insert_on_node(node.values[c], node)

        node.values.clear
            
    def query_closest_cell(self,x,y):
         # number of pixels in each left right up and down for the container search.
        initial_dimensions = self.maximum_area

        expansion_positive_x = x+initial_dimensions 
        expansion_negative_x = x-initial_dimensions

        expansion_positive_y = y+initial_dimensions
        expansion_negative_y = y-initial_dimensions

        # build the inital expansions
        if ( expansion_positive_x > self.parent_container[2] ):
            expansion_positive_x = self.parent_container[2] 
        if ( expansion_negative_x < self.parent_container[0] ):
            expansion_negative_x = self.parent_container[0]
        if ( expansion_positive_y > self.parent_container[3] ):
            expansion_positive_y = self.parent_container[3] 
        if ( expansion_negative_y < self.parent_container[1] ):
            expansion_negative_y = self.parent_container[1]

        minimum_id = [1000, 0]

        self.search_minimum_container(minimum_id, [expansion_negative_x, expansion_negative_y, expansion_positive_x, expansion_positive_y], (x,y), self.root)
    
        return minimum_id[0]
        

    def update_minimum_distance(self, minimum_id, point, node):

        for v in range(0, len(node.values)):
            
            inner_node = node.values[v]
            container = inner_node.container
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

            #node.value.display()
            distance, min_point = inner_node.value.point_distance( closest_point, point )

            if ( distance < minimum_id[0] ):
                minimum_id[0] = distance
                minimum_id[1] = node
    
    def search_minimum_container(self, minimum_id, container, point, node):

        if ( container_intersect(container, node.container ) ):

            if ( node.leaf == True ):

                self.update_minimum_distance(minimum_id, point, node)

            else:
                for i in range(0, len(node.children)):
                    if ( container_intersect(container, node.children[i].container) ):
                        self.search_minimum_container(minimum_id, node.children[i].container, point, node.children[i])


    def insert_on_node(self, current_node, to_node ):

        current_container = current_node.container

        if ( to_node.leaf == True ):

            if ( len(to_node.values) >= self.max_size ):
                self.redistribute( to_node )
                self.insert_on_node(current_node, to_node)
            else:
                to_node.values.append(current_node)
            return
        else:
            for c in range(0, len(to_node.children)):
                child_box = to_node.children[c].container
                if ( container_intersect( current_container, child_box ) ):
                    self.insert_on_node( current_node,  to_node.children[c] )

