class rb_node:
    intV = None
    left = None
    color = None
    right = None
    parent = None
    subset = None
    value = None

    def __init__(self,n):
        self.value = n
        self.color = 1
    
    def uncle(self):
        if(self.parent == None or self.parent.parent == None):
            return None
        if(self.parent.isOnLeft()):
            return self.parent.parent.right
        else:
            return self.parent.parent.left
    
    def isOnLeft(self):
        return self.left
    
    def sibling(self):
        if(self.parent == None):
            return None
        if(self.isOnLeft()):
            return self.parent.right
        return self.parent.left
    
    def moveDown(self,nParent):
        if(self.parent != None):
            
            if(self.isOnLeft()):
                self.parent.left = nParent
            else:
                self.parent.right = nParent
        
        nParent.parent = self.parent
        self.parent = nParent

    def hasRedChild(self):
        return (self.left != None and self.left.color == 1) or (self.right != None and self.right.color == 1)

class rb_tree:
    root = None
    elements = 0
    compare_func = None

    def __init__(self,_compare_func):
        self.root = None
        self.elements = 0
        self.compare_func = _compare_func
        return
    
    def leftRotate(self,x):
        nParent = x.right

        if(x == self.root):
            self.root = nParent

        x.moveDown(nParent)

        x.right = nParent.left

        if(nParent.left != None):
            nParent.left.parent = x
        
        nParent.left = x

    def rightRotate(self,x):
        nParent = x.left

        if(x == self.root):
            self.root = nParent
        
        x.moveDown(nParent)

        x.left = nParent.right

        if(nParent.right != None):
            nParent.right.parent = x
        
        nParent.right = x

    def swapColors(self,x1,x2):
        temp = x1.color
        x1.color = x2.color
        x2.color = temp

    def swapValues(self,u,v):
        temp = u.value
        u.value = v.value
        v.value = temp

    def fixRedRed(self,x):

        if(x == self.root):
            x.color = 0
            return
        
        parent = x.parent
        grandparent = parent.parent
        uncle = x.uncle()

        if(parent.color != 0):
            if(uncle != None and uncle.color == 1):
                parent.color = 0
                uncle.color = 0
                grandparent.color = 1
                self.fixRedRed(grandparent)
            else:
                if(parent.isOnLeft()):
                    if(x.isOnLeft()):
                        self.swapColors(parent,grandparent)
                    else:
                        self.leftRotate(parent)
                        self.swapColors(x,grandparent)

                    self.rightRotate(grandparent)
                else:
                    if(x.isOnLeft()):
                        self.rightRotate(parent)
                        self.swapColors(x,grandparent)
                    else:
                        self.swapColors(parent,grandparent)
                    
                    self.leftRotate(grandparent)

    def successor(self,x):
        temp = x
        while(temp.left != None):
            temp = temp.left
        
        return temp
    
    def BSTreplace(self,x):

        if(x.left != None and x.right != None):
            return self.successor(x.right)
        
        if(x.left != None and x.right == None):
            return None
        
        if(x.left != None):
            return x.left
        else:
            return x.right
    
    def fixDoubleBlack(self,x):
        if(x == self.root):
            return
        sibling = x.sibling()
        parent = x.parent
        if(sibling == None):
            self.fixDoubleBlack(parent)
        else:
            if(sibling.color == 1):
                parent.color = 1
                sibling.color = 0

                if(sibling.isOnLeft()):
                    self.rightRotate(parent)
                else:
                    self.leftRotate(parent)
                self.fixDoubleBlack(x)
            else:
                if(sibling.hasRedChild()):
                    if(sibling.left != None and sibling.left.color == 1):
                        if(sibling.isOnLeft()):
                            sibling.left.color = sibling.color
                            sibling.color = parent.color
                            self.rightRotate(parent)
                        else:
                            sibling.left.color = parent.color
                            self.rightRotate(sibling)
                            self.leftRotate(parent)
                    else:
                        if(sibling.isOnLeft()):
                            sibling.right.color = parent.color
                            self.leftRotate(sibling)
                            self.rightRotate(parent)
                        else:
                            sibling.right.color = sibling.color
                            sibling.color = parent.color
                            self.leftRotate(parent)
                    parent.color = 0
                else:
                    sibling.color = 1
                    if(parent.color == 1):
                        self.fixDoubleBlack(parent)
                    else:
                        parent.color = 0
     
    def deleteNode(self,v):
        u = self.BSTreplace(v)

        uvBlack = ((u == None) or u.color == 0) and (v.color == 0)
        parent = v.parent

        if(u == None):
            if(v == self.root):
                self.root = None
            else:
                if(uvBlack):
                    self.fixDoubleBlack(v)
                else:
                    if(v.sibling() != None):
                        v.sibling().color = 1
                if(v.isOnLeft()):
                    parent.left = None
                else:
                    parent.right = None

            return
        
        if(v.left == None or v.right == None):
            if(v == self.root):
                v.value = u.value
                v.left = None
                v.right = None
            else:
                if(v.isOnLeft()):
                    parent.left = u
                else:
                    parent.right = u

                u.parent = parent

                if(uvBlack):
                    self.fixDoubleBlack(u)
                else:
                    u.color = 0
            return

        self.swapValues(u,v)

        self.deleteNode(u)        

    def search(self,n):
        temp = self.root
        compar = 0
        lr = 0
        while(temp != None):
            compar = self.compare_func(n,temp.value)
            if(compar == 1):
                if(temp.left == None):
                    lr = 1
                    break
                else:
                    temp = temp.left
            elif(compar == 2):
                if(temp.right == None):
                    lr = 2
                    break
                else:
                    temp = temp.right
            else:
                lr = 0
                break

        return temp,lr

    def insert(self,n):
        node = segment_rb_node(n)
        if(self.root == None):
            node.color = 0 
            self.root = node
            self.elements+=1
        else:
            temp,lr = self.search(n)
            node.parent = temp
            if(lr == 0):
                return
            if(lr == 1):
                temp.left = node
            else:
                temp.right = node
            
            self.fixRedRed(node)
            self.elements += 1

    def deleteByVal(self,n):
        if(self == None):
            return
        
        v,lr = self.search(n)

        if(v.value != n):
            return
        
        self.deleteNode(v)
