# A heap which supports min and max heap but also semi efficent removal by id, but no heap sort

class tech_heap_node:

    def __init__(self, value, key):
        
        self.value = value
        self.key = key

        self.index = [0]

        return
    

class tech_heap:
    def __init__(self, type):
        
        # type either min or max
        if ( type == "max") :
            self.type = 1
        elif ( type == "min" ) :
            self.type = 0
        else:
            self.type = 1

        # tree array
        self.tree = []
        # tree nodes state
        self.tree_nodes_state = 0
        self.tree_capacity = 0
        return
    
    def resize(self):
        
        new_array = [0]*(max(1,self.tree_capacity)*2)

        for i in range(0, len(self.tree_nodes_state)):
            new_array[i] = self.tree[i]

        self.tree = new_array

        return
        
    def check_resize(self):
        
        if ( self.tree_nodes_state+1 > self.tree_capacity ):
            self.resize()

    def insert(self, value, key):
        
        self.check_resize()

        if (self.tree_nodes_state == 0):
            self.tree[0] = tech_heap_node(value, key)
            self.tree_nodes_state += 1
            return 0
        
        # create the node object
        the_node = tech_heap_node(value, key)
        # set the node reference index to where it is in the tree
        the_node.index[0] = self.tree_node_state

        self.tree[self.tree_nodes_state] = the_node

        self.heap_invariant(self.tree_nodes_state)

        self.tree_nodes_state += 1        

        return the_node.index
    
    def heap_invariant(self, index):
        
        current_key = self.tree[index].key

        parent_index = index/2

        parent_is_indexable = parent_index >= 0

        while ( parent_is_indexable ):
            
            parent_key = self.tree[parent_index].key
            parent_invariant = 0

            # is max invariant
            if ( self.type == 1 ) : parent_invariant = (parent_key < current_key)
            else : parent_invariant = (parent_key > current_key)

            if ( self.tree[parent_index] == 0 ):
                # move the node up to the parent and set its index pointer
                self.tree[index].index[0] = parent_index
                
                self.tree[parent_index] = self.tree[index]
                self.tree[index] = 0
            elif ( parent_invariant == 1 ):
                temp = self.tree[parent_index]
                self.tree[parent_index] = self.tree[index]
                self.tree[index] = temp
            else:
                break

            index = index/2
            parent_index = index/2

        return