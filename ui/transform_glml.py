import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from parse_glml import *
from state.state import *

class transform_glml:
    def __init__(self):
        return
    
    
    

document_tree = parse_glml("<el box=(1vw,2vw,3vw,4vw)> text_content <el> child  </el> </el>")

psuedo_state = state()
    
