import numpy as np
import os
import sys

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

class element_mesh:

    def __init__(self):

        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)

    def update(self, vertex_data, element_data, layout, layout_size):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, element_data.nbytes, element_data, GL_STATIC_DRAW)
        return

    def init_buffers(self, vertex_data, element_data, layout, layout_size):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, element_data.nbytes, element_data, GL_STATIC_DRAW)

        type_memory_map = {
            GL_FLOAT: 4,
            GL_UNSIGNED_INT: 4
        }
        
        memory_covered = 0
        for i in range(0, len(layout)):
            spread = layout[i][0]
            data_type = layout[i][1]

            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i, spread, data_type, GL_FALSE, layout_size, ctypes.c_void_p(memory_covered))
            memory_covered += spread*type_memory_map[data_type]

    def bind_for_draw(self):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)

        return


class text_cursor:

    def __init__(self, state, font):
        self.state = state
        self.font = font

        self.cursor_information = np.array([0.0, 0.0, 1.0, 0.0], dtype=np.float32)
        self.element_mesh = element_mesh()


        self.vertex_data = np.array([], dtype=np.float32)
        self.element_data = np.array([],dtype=np.uint32)

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0   

        self.update_program()
        self.generate_mesh()
        

        return
    
    def update_program(self):

        vertex_shader = '''
        #version 460 core\n
        layout(location = 0) in vec4 vertex;\n
        uniform vec4 cursor_information;\n
        out vec2 TexCoord;\n

        void main()\n
        {\n
            TexCoord = vertex.zw;\n
            gl_Position = vec4((vertex.x*cursor_information.z)+cursor_information.x, (vertex.y*cursor_information.z)+cursor_information.y, 0.0, 1.0);\n
        }\n



        '''

        fragment_shader = '''
        #version 460 core\n

        in vec2 TexCoord;\n
        uniform sampler2D atlas;\n
        uniform float time;\n
        
        void main()\n
        {\n
            float density = texture(atlas, TexCoord).r;
            gl_FragColor = vec4(1.0, 0.0, 0.0, density*abs(cos(time)));
        }\n

        '''
        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])

        return

    def append_point(self, x,y,uvx,uvy):

        self.vertex_data[self.vertex_index] = x
        self.vertex_data[self.vertex_index+1] = y
        self.vertex_data[self.vertex_index+2] = uvx
        self.vertex_data[self.vertex_index+3] = uvy

        self.vertex_index += 4

        return

    def append_character(self, char):
        
        width = char[4]
        height = char[5]
        bearingX = char[6]
        bearingY = char[7]

        self.append_point(bearingX, bearingY, char[0], char[1])
        self.append_point( bearingX + width,  bearingY, char[2], char[1])
        self.append_point( bearingX + width,  bearingY + height, char[2], char[3])
        self.append_point( bearingX,  bearingY + height, char[0], char[3])

        self.element_data[self.element_index] = self.current_element
        self.element_data[self.element_index+1] = self.current_element + 1
        self.element_data[self.element_index+2] = self.current_element + 2

        self.element_data[self.element_index+3] = self.current_element
        self.element_data[self.element_index+4] = self.current_element + 3
        self.element_data[self.element_index+5] = self.current_element + 2

        self.current_element += 4
        self.element_index += 6


        return



    def generate_mesh(self):

        atlas = self.state.texture_atlases[self.font][0]
        cursor_char = atlas.charmap[124]

        self.vertex_data.resize(4*4, refcheck=False)
        self.element_data.resize(6, refcheck=False)
        

        if(cursor_char != None):
            self.append_character(cursor_char)
        else:
            raise RuntimeError("Cursor character not found in font atlas")
        
        self.element_mesh.init_buffers(self.vertex_data, self.element_data, [(4, GL_FLOAT)], 16)


    def draw(self):

        glUseProgram(self.program)
        self.element_mesh.bind_for_draw()

        glSetVec4(self.program, "cursor_information", self.cursor_information)
        atlas = self.state.texture_atlases[self.font]
        texture = atlas[0].atlas_texture
        unit = atlas[1]
        glBindTexture(GL_TEXTURE_2D,texture)
        glActiveTexture(GL_TEXTURE0 + unit)

        glSetInt(self.program, "atlas", unit)
        glSetFloat(self.program, "time", self.state.time)

        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)

        
        return

class text_display:

    def __init__(self, state, font):

        self.state = state
        self.font = font
        self.tracked_value = None

        self.location = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self.container = [ np.array([0.0, 0.0], dtype=np.float32), np.array([0.0, 0.0], dtype=np.float32) ]

        #graphics buffers - vertex, element, vertex array
        self.vertex_data = np.array([], dtype=np.float32)
        self.element_data = np.array([],dtype=np.uint32)

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0

        self.element_mesh = element_mesh()

        self.state.event_objects.append(self)

        #for automatic updates
        self.previous_tracked_value = None

        #cursor

        self.cursor = text_cursor(state, font)
        self.cursor_location = 0
        self.cursor_locations = []
        self.cursor_locations_tail = 0
        
        
        return

    def set_tracked_value(self, value):
        self.tracked_value = value
        self.previous_tracked_value = value[0]
        return
    
    def set_location(self, location):
        self.location = location
        return
    
    def set_size(self, size):
        self.size = size
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

    def append_character(self, char, cursor_element, size):
        
        width = char[4]*size
        height = char[5]*size
        bearingX = char[6]*size
        bearingY = char[7]*size

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

        void main()\n
        {\n
            float density = texture(atlas, TexCoord).r;
            gl_FragColor = vec4(1.0, 0.0, 0.0, density);
            //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
        }\n'''



        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
        return

    def generate_mesh(self):

        _atlas = self.state.texture_atlases[self.font]
        bitmap_atlas = _atlas[0]
        text_value = str(self.tracked_value[0])

        #change size of cursor
        self.cursor.cursor_information[2] = self.size
        self.cursor_locations_tail = 0


        #estimate size of bounding box and fit by width
        bounding_diagonal = (self.container[1] - self.container[0])
        
        #get character size of text
        text_char_length = len(text_value)

        #using the quadrature length of the text item, we update the arrays ready for the geometry
        self.update_arrays(text_char_length)
        
        cursor_element = [self.location[0],self.location[1]]

        for i in range(0, len(text_value)):
            character = ord(text_value[i])
        
            if character in bitmap_atlas.charmap:
                char = bitmap_atlas.charmap[character]

                #update character locations
                if(self.cursor_locations_tail > len(self.cursor_locations) - 1):
                    self.cursor_locations.append([cursor_element[0]+char[6],cursor_element[1]+char[7]])
                    self.cursor_locations_tail += 1
                else:    
                    self.cursor_locations[self.cursor_locations_tail] = [cursor_element[0],cursor_element[1]] 
                    self.cursor_locations_tail += 1

                    
                self.append_character(char, cursor_element, self.size)
                


                cursor_element[0] = cursor_element[0] + char[4]*self.size
        
        
        #generate the buffers if they don't exist
        self.element_mesh.init_buffers(self.vertex_data, self.element_data, [(4, GL_FLOAT)], 16)
        self.update_program()

        #set cursor to end
        self.cursor.cursor_information[0] = self.cursor_locations[self.cursor_locations_tail-1][0]
        self.cursor.cursor_information[1] = self.cursor_locations[self.cursor_locations_tail-1][1]

    def update_mesh(self):
        _atlas = self.state.texture_atlases[self.font]
        bitmap_atlas = _atlas[0]
        text_value = str(self.tracked_value[0])

        self.cursor.cursor_information[2] = self.size
        

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0

        #estimate size of bounding box and fit by width
        bounding_diagonal = (self.container[1] - self.container[0])
        
        #get character size of text
        text_char_length = len(text_value)

        #using the quadrature length of the text item, we update the arrays ready for the geometry
        self.update_arrays(text_char_length)
        
        cursor_element = [self.location[0],self.location[1]]

        for i in range(0, len(text_value)):
            character = ord(text_value[i])
        
            if character in bitmap_atlas.charmap:
                char = bitmap_atlas.charmap[character]

                #update character locations
                if(self.cursor_locations_tail > len(self.cursor_locations) - 1):
                    self.cursor_locations.append([cursor_element[0],cursor_element[1]])
                    self.cursor_locations_tail += 1
                else:    
                    self.cursor_locations[self.cursor_locations_tail] = [cursor_element[0],cursor_element[1]] 
                    self.cursor_locations_tail += 1

                self.append_character(char, cursor_element, self.size)

                cursor_element[0] = cursor_element[0] + char[4]*self.size
        
        self.element_mesh.update(self.vertex_data, self.element_data, [(4, GL_FLOAT)], 16)

        #set cursor to end
        self.cursor.cursor_information[0] = self.cursor_locations[self.cursor_locations_tail-1][0]
        self.cursor.cursor_information[1] = self.cursor_locations[self.cursor_locations_tail-1][1]

    def check_update(self):
        if(self.tracked_value[0] != self.previous_tracked_value):
            self.previous_tracked_value = self.tracked_value[0]
            self.update_mesh()
            
        return

    def on_mouse_move(self, x,y):
        
        #print(self.state.mx)
        if(x > self.container[0][0]):
            #self.tracked_value[0] = "on hover"
            return   
        else:
            #self.tracked_value[0] = "(" + str(self.state.mx) + ", " + str(self.state.my) + ")"
            return 

        return
    
    def on_key_event(self, key, action):
        
        if(action == glfw.PRESS):
            direction = -1 if key == glfw.KEY_LEFT else 1 if key == glfw.KEY_RIGHT else 0
            if(direction == 0) : return
            if(self.cursor_location + direction < 0 or self.cursor_location + direction > len(self.cursor_locations)-1):
                return
            self.cursor_location += direction
            self.cursor.cursor_information[0] = self.cursor_locations[self.cursor_location][0]
            self.cursor.cursor_information[1] = self.cursor_locations[self.cursor_location][1]
            
        return

    def draw(self):
        
        self.cursor.draw()
        
        self.check_update()

        glUseProgram(self.program)

        self.element_mesh.bind_for_draw()

        atlas = self.state.texture_atlases[self.font]
        texture = atlas[0].atlas_texture
        unit = atlas[1]
        glBindTexture(GL_TEXTURE_2D,texture)
        glActiveTexture(GL_TEXTURE0 + unit)

        glSetInt(self.program, "atlas", unit)
        glDrawElements(GL_TRIANGLES, len(self.element_data), GL_UNSIGNED_INT, None)


