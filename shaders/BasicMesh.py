import numpy as np
import os
import sys

# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

class BasicMesh:

    def __init__( self, geometry, material ):

        self.geometry = geometry
        self.material = material

    def render(self):

        self.material.program.use_program()
        self.geometry.element_buffer.bind_for_draw()

        #glUseProgram(self.material.program.program)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.geometry.element_buffer.element_buffer)

        glDrawElementsInstanced(GL_TRIANGLES, self.geometry.element_buffer.elements_index, GL_UNSIGNED_INT, None, 1)



