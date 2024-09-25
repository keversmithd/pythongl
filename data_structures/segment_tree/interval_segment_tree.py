import math
import copy
## Interval segment tree.

## EDGE CASES ARE NOT FULLY THOUGHT OUT, REQUIRES BETTER IDEA
## TOO MANY DUPLICATES

class interval_segment_node:

    # contains array of values
    # contains children segments which are split from the main segment.
    value = None
    values = None
    segment =  None
    children = None
    isLeaf = True
    parent = None

    # measures if the node needs to be recopied or not if reused.
    branch_number = 0

    # store a self reference pointer
    self_value = None

    # initalize values to empty array and continue
    def __init__(self):

        self.values = []
        self.segment = [0,0]

        self.self_value = self

        return

    def init_leaf_node( self, segment ):
        
        self.segment[0] = segment[0]
        self.segment[1] = segment[1]

        self.isLeaf = True

    def init_non_leaf_node( self, segment ):

        self.segment[0] = segment[0]
        self.segment[1] = segment[1]

        self.isLeaf = False
        self.children = [ 0, 0 ]
    
    def convert_leaf_node ( self ):

        self.children = [ 0,0 ]
        self.isLeaf = False


def segments_intersect( segmentA, segmentB ):

    if ( segmentA[0] <= segmentB[0] and segmentA[1] >= segmentB[0] ):
        return True
    if ( segmentA[0] >= segmentB[0] and segmentA[0] <= segmentB[1] ):
        return True
    if ( segmentA[1] <= segmentB[1] and segmentA[1] >= segmentB[0] ):
        return True
    
    return False

# returns 0 for right adjacent 1 for left adjacent, 2 for complete overlap, 3 for intersection with left end point same, 4 for intersection with right end point same, 5 for internal intersection, 6 inside to outside right, 7 outside to inside from the left
def segments_info( segmentA, segmentB ):

    # epsilon distance
    eps = 0.01

    # distance between start points of both segments
    d0 = math.fabs( segmentB[0] - segmentA[0] )
    # end points
    d1 = math.fabs ( segmentB[1] - segmentA[1] )

    # distance from start point of A to end point of B
    d2 = math.fabs ( segmentA[0] - segmentB[1] )
    # distance from end point of A to start point of B
    d3 = math.fabs ( segmentA[1] - segmentB[0] )

    # if the left end point of A is right end point of B and the right end point of A is greather than the right end point of B
    if ( d2 <= eps and segmentA[1] >= segmentB[1] ):
        return 0
    if ( d3 <= eps and segmentA[0] <= segmentB[0] ):
        return 1
    
    
    if ( segmentA[0] <= segmentB[0] and segmentA[1] >= segmentB[1] ):
        return 2
    
    if ( d0 < eps and ( segmentA[1] > segmentB[1] or segmentA[1] < segmentB[1] ) ):
        return 3
    
    if ( d1 < eps and ( segmentA[0] > segmentB[0] or segmentA[0] < segmentB[1] ) ):
        return 4
    
    if ( segmentA[0] > segmentB[0] and segmentA[1] < segmentB[1] ):
        return 5
    
    if ( (segmentA[0] > segmentB[0] and segmentA[0] < segmentB[1]) and ( segmentA[1] > segmentB[1] )):
        return 6
    
    if ( (segmentA[1] < segmentB[1] and segmentA[1] > segmentB[0]) and ( segmentA[0] < segmentB[0] )):
        return 7


def point_intersects_segment ( point, segment ):

    if ( point >= segment[0] and point <= segment[1] ):
        return True
    return False


# returns whether the two segments share a single end point, and which one, or both
def segment_boundary(segmentA, segmentB):

    spacial_limit = 0.001

    a_d = math.fabs(segmentB[0] - segmentA[0]) < spacial_limit # share left
    b_d = math.fabs(segmentB[1] - segmentA[1]) < spacial_limit # share right
    c_d = math.fabs(segmentB[1] - segmentA[0]) < spacial_limit # segmentA to the right of segment B
    d_d = math.fabs(segmentB[0] - segmentA[1]) < spacial_limit # segmentA to the left an


    if ( a_d  and b_d or ( c_d and d_d ) ):
        return "both"
    elif ( a_d and not b_d ):
        return "share_left"
    elif ( b_d and not a_d ):
        return "share_right"
    elif ( c_d and not d_d ):
        return "left_right"
    elif ( d_d and not c_d ):
        return "right_left"
    
    return "none"

# returns union of the two segments
def union_segments(segmentA, segmentB):

    x = min (segmentA[0], segmentB[0])
    y = max (segmentA[1], segmentB[1])

    return (x,y)

# returns the clipped union segment between A annd B
def clip_segment(segmentA, segmentB):

    x = max ( segmentA[0], segmentB[0] )
    y = min ( segmentA[1], segmentB[1] )

    return (x,y)

class interval_segment_tree:

    # generate none root.
    root = None

    # set the max limit of items in a node.

    # generates the root leaf node of the interval tree.
    def __init__(self):

  
        self.values_limit = 1

        self.elements = 0
        # store the amount of elements inserted

        return

    def segment_outside_root ( self, node ):

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( union_segments(node.segment, self.root.segment) )

        node.parent = new_root
        self.root.parent = new_root

        if ( node.segment[1] <= self.root.segment[0]  ):

            new_root.children[0] = node
            new_root.children[1] = self.root
            
        elif ( node.segment[0] >= self.root.segment[1] ):

            new_root.children[0] = self.root
            new_root.children[1] = node
        
        self.root = new_root

    def insert( self, segment, value ):


        if ( self.root == None ):
            root_node = interval_segment_node()
            root_node.init_leaf_node( segment )
            root_node.value = value
            self.root = root_node

            self.elements += 1
            return

        # initialized an unmoved node, if the node is inserted into one side of the tree, it's insert value is increased.
        node = interval_segment_node ( )
        node.init_leaf_node( segment )
        node.value = value

        # check segment intersection with the root node
        info = segments_info ( segment, self.root.segment )

        if ( info == None or info == 0 or info == 1 ):

            self.segment_outside_root ( node )
        else:
           
            self.insert_on_node ( node, self.root, info, -1 )

        self.elements += 1

    # handle right adjacent insertion
    def right_adj_insert( self, src_node, dst_node, leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.parent.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            
        # dst_node.parent = new_root
        # src_node.parent = new_root

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    def left_adj_insert (self, src_node, dst_node, leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.parent.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    # handle overlapped intersection
    def overlap_insert ( self, src_node, dst_node, leftright ):

        clipped_segment = dst_node.segment

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    def internal_insert ( self, src_node, dst_node,  leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( unionized_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root
        
    def left_latch_insert ( self, src_node, dst_node ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.parent.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    def right_latch_insert ( self, src_node, dst_node, leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.parent.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            
        dst_node.parent = new_root
        src_node.parent = new_root

        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    # from internal to external right
    def external_right_insert ( self, src_node, dst_node, leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.segment )

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )

        

        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1
            
        new_root.children[0] = dst_node
        new_root.children[1] = src_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root

    def external_left_insert ( self, src_node, dst_node, leftright ):

        unionized_segment = union_segments ( src_node.segment, dst_node.segment )
        # then clip it by the parent
        clipped_segment = clip_segment ( unionized_segment, dst_node.segment )

        

        new_root = interval_segment_node ( )
        new_root.init_non_leaf_node ( clipped_segment )


        if ( src_node.branch_number == 1 ):

            # then set src_node as a copy of src
            src_node = copy.copy(src_node)
        else:
            src_node.branch_number += 1


        new_root.children[0] = src_node
        new_root.children[1] = dst_node

        dst_node.parent.children[leftright] = new_root

        dst_node.parent = new_root
        src_node.parent = new_root
    # regular insert node, leftright for whether the node is left or a right child.
    def insert_on_node ( self, src_node, dst_node, info, leftright ):

        # src node container
        src_node_segment = src_node.segment

        # dst node container
        dst_node_segment = dst_node.segment

    
        if ( dst_node.isLeaf == True ):

            # unionize the leaf with the src

            if ( info == 0 ):
                # right adjacent then union
                self.right_adj_insert( src_node, dst_node, leftright )
            if ( info == 1 ):
                self.left_adj_insert( src_node, dst_node, leftright)
            if ( info == 2  ):
                self.overlap_insert ( src_node, dst_node, leftright )
            if ( info == 5 ):
                self.internal_insert ( src_node, dst_node, leftright )
            if ( info == 3 ):
                self.left_latch_insert ( src_node, dst_node, leftright )
            if ( info == 4 ):
                self.right_latch_insert ( src_node, dst_node, leftright )
            if ( info == 6 ):
                self.external_right_insert ( src_node, dst_node, leftright )
            if ( info == 7 ):
                self.external_left_insert ( src_node, dst_node, leftright )

        else:
            
            # store child segment0 and child segment1
            segment0 = dst_node.children[0].segment
            segment1 = dst_node.children[1].segment

            # gather segment intersection info
            info0 = segments_info ( src_node_segment, segment0 )
            info1 = segments_info ( src_node_segment, segment1 )

            # returns 0 for right adjacent 1 for left adjacent, 2 for complete overlap, 3 for intersection with left end point same, 4 for intersection with right end point same, 5 for internal intersection, 6 for inside to external intersection right, 7 for inside to external left

            if ( info0 == 2 ):
                self.insert_on_node( src_node, dst_node.children[0], info0, 0, info0, 0 )
            if ( info1 == 2 ):
                self.insert_on_node ( src_node, dst_node.children[1], info1,1 )

            if ( info0 == 4 ):
                self.insert_on_node ( src_node, dst_node.children[0], info0, 0 )
                return
            if ( info1 == 3 ):
                self.insert_on_node ( src_node, dst_node.children[1], info1,1 )
                return


            if ( info0 == 6 or info1 == 6 or info0 == 7 or info1 == 7):
                if ( info0 == 6 ):
                    self.insert_on_node ( src_node, dst_node.children[0], info0, 0 )
                
                if ( info1 == 6 ):
                    self.insert_on_node ( src_node, dst_node.children[1], info1, 1 )
                    
                if ( info0 == 7 ):
                    self.insert_on_node ( src_node, dst_node.children[0], info0, 0 )
                
                if ( info1 == 7 ):
                    self.insert_on_node ( src_node, dst_node.children[1], info1, 1 )
                

            if ( info0 == 5 ):
                self.insert_on_node ( src_node, dst_node.children[0], info0, 0 )
                return

            if ( info1 == 5 ):
                self.insert_on_node ( src_node, dst_node.children[1], info1, 1 )
                return
            
    # return list of all leaf nodes that the point intersects
    def query ( self, point ):   

        # collect the query results, would be best to maybe return reference so the value don't have to copied.
        query_results = []
        query_visited = {}

        # we query on the node.
        self.query_on_node ( self.root, point, query_results, query_visited )

        return query_results

    def query_on_node ( self, node, point, query_results, query_visited ):

        if ( point_intersects_segment( point, node.segment ) == False ):
            return

        if ( node.isLeaf == True ):

            if ( node.self_value not in query_visited):
                query_visited[node.self_value] = node
                query_results.append ( node )

        else:
            if ( point_intersects_segment( point, node.children[0].segment ) == True ):
                self.query_on_node ( node.children[0], point, query_results, query_visited )
            if ( point_intersects_segment ( point, node.children[1].segment ) == True ):
                self.query_on_node ( node.children[1], point, query_results, query_visited )

    


# tree = interval_segment_tree( )

# tree.insert ( (0.0, 0.5), "A")
# tree.insert ( (0.5, 1.0), "B")
# tree.insert ( (0.3, 0.8), "C")
# tree.insert ( (1.2, 1.8), "D")
# tree.insert ( (0.7, 1.4), "E")

# query_results = tree.query(0.5)
# query_results = tree.query(1.0)
# query_results = tree.query(1.4)

# print("End Test 1")