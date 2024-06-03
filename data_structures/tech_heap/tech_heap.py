# A heap which supports min and max heap but also semi efficent removal by id, but no heap sort

class tech_heap_node:

    def __init__(self, value, key):
        
        self.value = value
        self.key = key

        self.index = [0]

        return
    
# Tech Heap
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

        for i in range(0, self.tree_nodes_state):
            new_array[i] = self.tree[i]

        self.tree = new_array
        self.tree_capacity = (max(1,self.tree_capacity)*2)

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
        # de reference and this state of inside of the node will change.
        the_node.index[0] = self.tree_nodes_state

        # apply the node to end of the tree.
        self.tree[self.tree_nodes_state] = the_node

        # apply heap invariant.
        self.heap_invariant(self.tree_nodes_state)

        self.tree_nodes_state += 1        

        return the_node.index
    
    # bubble up
    def heap_invariant(self, index):
        
        # get key of current node, at the particular index.
        current_key = self.tree[index].key

       

        # inital state to one to do a pre-while loop. it being greater than zero should be guarenteed.
        parent_is_indexable = index > 0

        # while the process can access its parent.
        while ( parent_is_indexable ):
            
            # get parent index
            parent_index = int(index/2)

            # get parent key.
            parent_key = self.tree[parent_index].key
            # label a boolean.
            parent_invariant = 0

            # is max invariant else min invariant.
            if ( self.type == 1 ) : parent_invariant = (parent_key < current_key) # set boolean true if the parent is less than the current key.
            else : parent_invariant = (parent_key > current_key) # min invariant.

            # if the parent is empty or a zero for now.
            # CHANGE: Make node empty by variable rather than zero, and share node.
            if ( self.tree[parent_index] == 0 ):
                
                # move the node up to the parent and set its index pointer
                self.tree[index].index[0] = parent_index
                self.tree[parent_index] = self.tree[index]
                self.tree[index] = 0
                # CHANGE: shift the remaining branches up instead.

            elif ( parent_invariant == 1 ):
                
                temp = self.tree[parent_index]
                self.tree[parent_index] = self.tree[index]
                self.tree[index] = temp
            else:
                break

            index = int(index/2)
            parent_index = int(index/2)

            # if now the parent index is greater than zero continue to the top.
            parent_is_indexable = parent_index > 0

        return
    
    # comparative function based on heap type.
    def comparator(self, child_key, parent_key):
        
        if ( self.type == 1):
            return child_key > parent_key
        else:
            return child_key < parent_key

    # pull up, selects the next max child changes the parent out then follows the max child.
    def pull_up(self, index):
        
        # needs fixing incase the parent is zero, in that case 
        children_available = ( (index*2)+1 < self.tree_nodes_state or (index*2)+2 < self.tree_nodes_state )

        children = [0,0]

        parent = index

        

        while ( children_available ):
            
            # select best child
            best_child = 0
            best_child_key = 0 

            # reset the children array
            children[0] = 0
            children[1] = 0
            
            if ( (parent*2)+1 < self.tree_nodes_state ):
                if ( self.tree[(parent*2)+1] != 0):
                    children[0] = (index*2)+1
            if ( (parent*2)+2 < self.tree_nodes_state ):
                if ( self.tree[(parent*2)+2] != 0 ):
                    children[1] = (index*2)+2

            for child in children:
                if ( child != 0 and self.comparator( self.tree[child].key, best_child_key ) ):
                    best_child = child
                    best_child_key = self.tree[child].key

            if ( best_child != 0 ):
                self.tree[best_child].index = parent
                self.tree[parent] = self.tree[best_child]
                self.tree[best_child] = self.tree[parent]

            children_available = ( (parent*2)+1 < self.tree_nodes_state or (parent*2)+2 < self.tree_nodes_state )

            if ( best_child == 0 and children_available ):
                parent = best_child
            else:
                parent = best_child
                
            

                    
            
        


    # returns root of heap then the next child needs to be selected to be at the top of the list.
    def pop(self):
        
        # get the root node
        the_node = self.tree[0]

        # a boolean to check if any children exist.
        children_exist = 0

        if ( 1 < self.tree_nodes_state and 2 >= self.tree_nodes_state ):
            self.tree[1].index = 0
            self.tree[0] = self.tree[1]
            self.tree[1] = 0

            children_exist = 1
        elif ( self.type == 1 ):
            
            children_exist = 2
            if ( self.tree[1].key > self.tree[2].key ):
                self.tree[1].index = 0
                self.tree[0] = self.tree[1]
                self.tree[1] = 0
            else:
                self.tree[2].index = 0
                self.tree[0] = self.tree[2]
                self.tree[2] = 0
            
        

        if ( children_exist and self.tree[0] != 0 ):
            self.tree[children_exist].index = 0
            self.tree[0] = self.tree[children_exist]
            

        return the_node

t = tech_heap("max")

t.insert("a",3)
t.insert("b",4)
t.insert("c",2)

print ( t.pop().value )
