from octree_bounding import *

class Octnode:
    bounding_domain = [[0,0,0],[0,0,0]]
    value = 0

    def __init__(self, value, bounding):
        self.bounding_domain = bounding
        self.value = value

max_octree_entries = 12

class Octree:
    bounding_domain = [[0,0,0],[0,0,0]]
    split_domain = None

    entries = []

    children = [None,None,None,None,
                None,None,None,None]
    
    leaf = False
    
    def __init__(self, bounding_domain):
        self.bounding_domain = bounding_domain

    def __init__(self, value):
        self.leaf = True
        self.entries.append(value)

    def insert_triangle(self, triangle):
        triangle_bounding = bounding_from_triangle(triangle)
        triangle_node = Octnode(triangle,triangle_bounding)
        self.insert_node(triangle_node)
    
    def insert_node(self, node):
        
        if(self.split_domain == None):
            self.split_domain = split_bounding(self.bounding_domain)
        intersection_list = bounding_intersection_list(self.split_domain, node.bounding_domain)
        for i in range(0, len(intersection_list)):
            intersection_id = intersection_list[i]
            if(self.children[intersection_id] == None):
                self.children[intersection_id] = Octree(node)
            elif(self.children[intersection_id].leaf == True):
                if(len(self.children[intersection_id].entries) >= max_octree_entries):
                    self.children[intersection_id].redistribute()
                else:
                    self.children[intersection_id].entries.append(node)
            else:
                self.children[intersection_id].insert_node(node)
        

    def redistribute(self):
        for i in range(len(self.entries),0,-1):
            self.insert_node(self.entries[i])
            self.entries.pop()
        self.leaf = False

            

            
        


    