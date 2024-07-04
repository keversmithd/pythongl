import os
import sys
import random
import numpy as np

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

from state.state import *

class UniformBuffer:
    def __init__(self, state, data = None):
        
        self.state = state

        # Store the uniform buffer and the block index
        self.uniform_buffer = 0

        # Go ahead and generate the buffer
        self.create_buffer()

        # Generate and store the uniform buffer index from the state so that it is unique
        self.uniform_index = state.add_uniform_buffer()

        if data != None:
            self.set_buffer(data)

        return
    
    def create_buffer(self):
        self.uniform_buffer = glGenBuffers(1)

    def set_buffer(self,data):

        glBindBuffer(GL_UNIFORM_BUFFER, self.uniform_buffer)
        glBufferData(GL_UNIFORM_BUFFER, data.nbytes, data, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_UNIFORM_BUFFER, 0)

        return