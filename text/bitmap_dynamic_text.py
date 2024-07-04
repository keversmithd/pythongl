import numpy as np
import os
import sys

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

class text_display:

    def __init__(self, state, font):

        self.state = state
        self.font = font
        self.tracked_value = None

        self.location = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.container = [np.array([0.0, 0.0, 0.0], dtype=np.float32),np.array([0.0, 0.0, 0.0], dtype=np.float32)]


        #graphics buffers - vertex, element, vertex array
        self.vertex_data = np.array([], dtype=np.float32)
        self.element_data = np.array([],dtype=np.uint32)

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0

        self.basic_element_mesh = basic_element_mesh()


        #for automatic updates
        self.previous_tracked_value = None
        
        return

    def set_tracked_value(self, value):
        self.tracked_value = value
        self.previous_tracked_value = value[0]
        return
    
    def set_location(self, location):
        self.location = location
        return
    
    def set_container(self, container):
        self.container = container
        return
    
    def update_arrays(self, quadrature_length):
        
        self.vertex_data.resize(quadrature_length*4*4, refcheck=False)
        self.element_data.resize(quadrature_length*6, refcheck=False)


        return

    def append_point(self, x,y,uvx,uvy):

        self.vertex_data[self.vertex_index] = x
        self.vertex_data[self.vertex_index+1] = y
        self.vertex_data[self.vertex_index+2] = uvx
        self.vertex_data[self.vertex_index+3] = uvy

        self.vertex_index += 4

        return

    def append_character(self, char, cursor_element):
        
        width = char[4]
        height = char[5]
        bearingX = char[6]
        bearingY = char[7]

        self.append_point(cursor_element[0] + bearingX, cursor_element[1] + bearingY, char[0], char[1])
        self.append_point(cursor_element[0] + bearingX + width, cursor_element[1] + bearingY, char[2], char[1])
        self.append_point(cursor_element[0] + bearingX + width, cursor_element[1] + bearingY + height, char[2], char[3])
        self.append_point(cursor_element[0] + bearingX, cursor_element[1] + bearingY + height, char[0], char[3])

        
        self.element_data[self.element_index] = self.current_element
        self.element_data[self.element_index+1] = self.current_element + 1
        self.element_data[self.element_index+2] = self.current_element + 2

        self.element_data[self.element_index+3] = self.current_element
        self.element_data[self.element_index+4] = self.current_element + 3
        self.element_data[self.element_index+5] = self.current_element + 2

        self.current_element += 4
        self.element_index += 6


        return

    def update_program(self):


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

        out vec4 frag_color;

        void main()\n
        {\n
            float density = texture(atlas, TexCoord).r;
            frag_color = vec4(1.0, 0.0, 0.0, density);
            //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }\n'''



        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
        return

    def generate_mesh(self):

        _atlas = self.state.texture_atlases[self.font]
        bitmap_atlas = _atlas[0]
        text_value = str(self.tracked_value[0])

        #estimate size of bounding box and fit by width
        bounding_diagonal = (self.container[1] - self.container[0])
        
        #get character size of text
        text_char_length = len(text_value)

        #using the quadrature length of the text item, we update the arrays ready for the geometry
        self.update_arrays(text_char_length)
        
        cursor_element = [0,0]

        for i in range(0, len(text_value)):
            character = ord(text_value[i])
        
            if character in bitmap_atlas.charmap:
                char = bitmap_atlas.charmap[character]

                self.append_character(char, cursor_element)

                cursor_element[0] = cursor_element[0] + char[4]
        
        
        #generate the buffers if they don't exist
        self.basic_element_mesh.init_buffers(self.vertex_data, self.element_data, [(4, GL_FLOAT)], 16)
        self.update_program()

    def update_mesh(self):
        _atlas = self.state.texture_atlases[self.font]
        bitmap_atlas = _atlas[0]
        text_value = str(self.tracked_value[0])

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0

        #estimate size of bounding box and fit by width
        bounding_diagonal = (self.container[1] - self.container[0])
        
        #get character size of text
        text_char_length = len(text_value)

        #using the quadrature length of the text item, we update the arrays ready for the geometry
        self.update_arrays(text_char_length)
        
        cursor_element = [0,0]

        for i in range(0, len(text_value)):
            character = ord(text_value[i])
        
            if character in bitmap_atlas.charmap:
                char = bitmap_atlas.charmap[character]

                self.append_character(char, cursor_element)

                cursor_element[0] = cursor_element[0] + char[4]
        
        self.basic_element_mesh.update(self.vertex_data, self.element_data, [(4, GL_FLOAT)], 16)

    def check_update(self):
        if(self.tracked_value[0] != self.previous_tracked_value):
            self.previous_tracked_value = self.tracked_value[0]
            self.update_mesh()
            
        return

    def draw(self):
        
        self.check_update()

        glUseProgram(self.program)

        self.basic_element_mesh.bind_for_draw()

        atlas = self.state.texture_atlases[self.font]
        texture = atlas[0].atlas_texture
        unit = atlas[1]
        glBindTexture(GL_TEXTURE_2D,texture)
        glActiveTexture(GL_TEXTURE0 + unit)

        
        glSetInt(self.program, "atlas", unit)
        glDrawElements(GL_TRIANGLES, len(self.element_data), GL_UNSIGNED_INT, None)


