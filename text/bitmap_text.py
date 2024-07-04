import os
import sys
import numpy as np
import ctypes

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from state.state import *
from shaders.PyGLHelper import *


class bitmap_text:

    def __init__(self, state):
        self.state = state

        self.vertex_array = 0
        self.vertex_buffer = 0
        self.element_buffer = 0
        self.program = 0

        self.vertex_data = []
        self.element_data = []
        self.element_index = 0

        return
    

    def setup_render(self):

        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)

        vertex_shader = '''
        #version 460 core\n
        layout(location = 0) in vec4 vertex;\n

        out vec2 TexCoord;\n
        void main(){\n
            gl_Position = vec4(vertex.xy, 0.0, 1.0);\n
            TexCoord = vertex.zw;\n
            


        }\n
        '''

        fragment_shader = '''
        #version 460 core\n
        in vec2 TexCoord;\n
        

        uniform sampler2D atlas;\n

        void main()\n
        {\n
            float density = texture(atlas, TexCoord).r;
            gl_FragColor = vec4(1.0, 0.0, 0.0, density);
        }\n'''



        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])

    def render_text(self, text, font):

        self.font = font
        texture_atlas = self.state.texture_atlases[font]
        if(texture_atlas == None):
            print("Texture atlas not found in state")
            return

        cursor_element = [0,0]

        bitmap_atlas = texture_atlas[0]

        for i in range(0, len(text)):
            character = ord(text[i])
        
            if character in bitmap_atlas.charmap:
                char = bitmap_atlas.charmap[character]

                self.append_character(char, cursor_element, char[4], char[5], char[6], char[7])

                cursor_element[0] = cursor_element[0] + char[4]
        
        self.setup_render()
        self.setup_buffers()

        return


    def setup_buffers(self):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer) 
        glBufferData(GL_ARRAY_BUFFER, len(self.vertex_data)*4, np.array(self.vertex_data,dtype=np.float32), GL_STATIC_DRAW)



        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(self.element_data)*4, np.array(self.element_data, dtype=int), GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4*4, ctypes.c_void_p(0))
 
    def draw(self):

        glUseProgram(self.program)
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        
        atlas = self.state.texture_atlases[self.font]
        texture = atlas[0].atlas_texture
        unit = atlas[1]
        glBindTexture(GL_TEXTURE_2D,texture)
        glActiveTexture(GL_TEXTURE0 + unit)

        glSetInt(self.program, "atlas", unit)

        glDrawElements(GL_TRIANGLES, len(self.element_data), GL_UNSIGNED_INT, None)
        

    def append_character(self,char, position, width, height, bearingX, bearingY):

        self.vertex_data.append( position[0] + bearingX )
        self.vertex_data.append( position[1] + bearingY )
        self.vertex_data.append( char[0] )
        self.vertex_data.append( char[1] )

        self.vertex_data.append( position[0] + bearingX + width  )
        self.vertex_data.append( position[1] + bearingY )
        self.vertex_data.append( char[2])
        self.vertex_data.append( char[1])

        self.vertex_data.append(position[0] + bearingX + width  )
        self.vertex_data.append( position[1] + bearingY + height)
        self.vertex_data.append( char[2])
        self.vertex_data.append( char[3])

        self.vertex_data.append(position[0] + bearingX)
        self.vertex_data.append( position[1] + bearingY + height)
        self.vertex_data.append( char[0])
        self.vertex_data.append( char[3])

        

        self.element_data.append(self.element_index)
        self.element_data.append(self.element_index+1)
        self.element_data.append(self.element_index+2)

        self.element_data.append(self.element_index+2)
        self.element_data.append(self.element_index+3)
        self.element_data.append(self.element_index)

        self.element_index += 4


        return



                

        

