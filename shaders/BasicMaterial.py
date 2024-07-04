
import numpy as np
import os
import sys

# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

from shaders.ShaderProgram import *

class BasicMaterial:

    def __init__(self, state):

        self.program = None
        self.state = state

        self.make_program()

    def make_program(self):


        vertex_shader = '''
            #version 460 core

            layout(location = 0) in vec3 position;
            layout(location = 1) in vec3 normal;
            layout(location = 2) in vec2 uv;
        
            uniform mat4 projection;
            uniform mat4 view;

            out vec2 o_uv;

            void main()
            {
                o_uv = uv;
                gl_Position = view*projection*vec4(position, 1.0);

            }

        '''

        fragment_shader = '''
            #version 460 core

            in vec2 o_uv;

            out vec4 color;
            void main()
            {

                color = vec4(o_uv, 0.0, 1.0);

            }

        '''

        self.program = ShaderProgram({
            "vertex_shader" : vertex_shader,
            "fragment_shader" : fragment_shader,
            "camera" : [ self.state.active_camera ]
        })
    
    