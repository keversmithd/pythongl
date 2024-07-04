import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

# import the dequeue module.
from collections import deque

from parse_glml import *
from state.state import *

# Import the ui element machine in order to communicate and generate some layout ui elements
from ui.layout_element_machine import *

# import the layout object, should/could have a more interesting like connection object.
# the connection object will listen for calls and will interface between the transformer and the state object for rendering calls.
from layout_element import *

class transform_glml:
    def __init__(self, state):
        # set the state up correctly.
        self.state = state
        return

    # takes a glml string builds the document tree and then transforms/renders the output
    def render(self, glml_string ):
        # get the document tree state from parse_glml
        document_tree = parse_glml(glml_string)
        # then transform or add.
        self.transform(document_tree)


    def transform( self, document_tree ):
        # traverse document_tree
        # creating elements in scene_context at each node
        # and then just setting the previous parent as the attribute.

        root = document_tree.root
        # check if the root is null
        if ( root == None ):
            print("TRANSFORM_GLML: Bad root")
            return

        # use breadth first on the elements

            

        return
    



    
