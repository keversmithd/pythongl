import os
import sys

# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

from shaders.ElementBuffer import InterleavedElementBuffer

class cube_geometry:

    def __init__(self):

        self.element_buffer = InterleavedElementBuffer({
            "position" : 3,
            "normal" : 3,
            "uv" : 2
        })

        self.generate_geometry()

        return
    def generate_geometry(self):

        self.element_buffer.allocate(24)

        self.element_buffer.push("position", [ -1.0, -1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, -1.0 ] )
        self.element_buffer.push("uv", [ 0.0, 0.0 ] )

        self.element_buffer.push("position", [ 1.0, -1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, -1.0 ] )
        self.element_buffer.push("uv", [ 1.0, 0.0 ] )

        self.element_buffer.push("position", [ 1.0, 1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, -1.0 ] )
        self.element_buffer.push("uv", [ 1.0, 1.0 ] )

        self.element_buffer.push("position", [ -1.0, 1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, -1.0 ] )
        self.element_buffer.push("uv", [ 0.0, 1.0 ] )

        self.element_buffer.push_index([0,1,2,0,2,3], 4)

        self.element_buffer.push("position", [ -1.0, -1.0, 0.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, 1.0 ] )
        self.element_buffer.push("uv", [ 0.0, 0.0 ] )

        self.element_buffer.push("position", [ 1.0, -1.0, 0.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, 1.0 ] )
        self.element_buffer.push("uv", [ 1.0, 0.0 ] )

        self.element_buffer.push("position", [ 1.0, 1.0, 0.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, 1.0 ] )
        self.element_buffer.push("uv", [ 1.0, 1.0 ] )

        self.element_buffer.push("position", [ -1.0, 1.0, 0.0 ] )
        self.element_buffer.push("normal", [ 0.0, 0.0, 1.0 ] )
        self.element_buffer.push("uv", [ 0.0, 1.0 ] )

        self.element_buffer.push_index([0,1,2,0,2,3], 4)

        

        self.element_buffer.push("position", [ -1.0, 1.0, 0 ] )
        self.element_buffer.push("normal", [ 0.0, 1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, 1.0, 0 ] )
        self.element_buffer.push("normal", [ 0.0, 1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, 1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 1.0 ] )
        self.element_buffer.push("position", [ -1.0, 1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, 1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 1.0 ] )



        self.element_buffer.push_index([0,1,2,0,2,3], 4)

        self.element_buffer.push("position", [ -1.0, -1.0, 0 ] )
        self.element_buffer.push("normal", [ 0.0, -1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, -1.0, 0 ] )
        self.element_buffer.push("normal", [ 0.0, -1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, -1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, -1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 1.0 ] )
        self.element_buffer.push("position", [ -1.0, -1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 0.0, -1.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 1.0 ] )



        self.element_buffer.push_index([0,1,2,0,2,3], 4)

        # self.element_buffer.push("position", [ -1.0, -1.0, -1.0 ] )
        # self.element_buffer.push("normal", [ -1.0, 0.0, 0.0 ] )
        # self.element_buffer.push("uv", [ 0.0, 0.0 ] )
        # self.element_buffer.push("position", [ -1.0, -1.0, 0 ] )
        # self.element_buffer.push("normal", [ -1.0, 0.0, 0.0 ] )
        # self.element_buffer.push("uv", [ 1.0, 0.0 ] )
        # self.element_buffer.push("position", [ -1.0, 1.0, 0 ] )
        # self.element_buffer.push("normal", [ -1.0, 0.0, 0.0 ] )
        # self.element_buffer.push("uv", [ 1.0, 1.0 ] )
        # self.element_buffer.push("position", [ -1.0, 1.0, -1.0 ] )
        # self.element_buffer.push("normal", [ -1.0, 0.0, 0.0 ] )
        # self.element_buffer.push("uv", [ 0.0, 1.0 ] )



        # self.element_buffer.push_index([0,1,2,0,2,3], 4)

        self.element_buffer.push("position", [ 1.0, -1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 1.0, 0.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, -1.0, 0 ] )
        self.element_buffer.push("normal", [ 1.0, 0.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 0.0 ] )
        self.element_buffer.push("position", [ 1.0, 1.0, 0 ] )
        self.element_buffer.push("normal", [ 1.0, 0.0, 0.0 ] )
        self.element_buffer.push("uv", [ 1.0, 1.0 ] )
        self.element_buffer.push("position", [ 1.0, 1.0, -1.0 ] )
        self.element_buffer.push("normal", [ 1.0, 0.0, 0.0 ] )
        self.element_buffer.push("uv", [ 0.0, 1.0 ] )

        self.element_buffer.push_index([0,1,2,0,2,3], 4)

        self.element_buffer.sync_buffers()


    
