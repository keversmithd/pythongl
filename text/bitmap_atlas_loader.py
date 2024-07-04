import freetype
import os
import sys
import ctypes
import numpy as np

from collections import deque

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

# charmap has the format
# u,v [bottom_left]
# u,v [top_right]
# normalized width, normalized height
# left advance, vertical advance

class bitmap_atlas:
    charmap = None
    char_ranges = None
    atlas_texture = None
    texture_unit = None

    def __init__(self, charmap, char_ranges, atlas_texture):
        self.charmap = charmap
        self.char_ranges = char_ranges
        self.atlas_texture = atlas_texture


# bitmap atlas loader generates a bitmap atals as specified above.
class bitmap_atlas_loader:
    char_ranges = [[32,122]]
    chars_loaded = 0
    charmap = {}
    texture_data = None

    # font is the font path, resolution is the size of the bitmap resolution
    # the margin is the space between each character.
    def __init__(self, state, atlas_name, font, resolution = [512, 512], horizontal_margin = 10, vertical_margin = 10, font_size=48):

        self.font = font
        self.resolution = resolution
        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin
        self.font_size = font_size
        self.atlas_name = atlas_name
        self.state = state

        self.make_atlas()

    
    # Inserts a character token into the bitmap text generated upon init.
    def insert_bitmap(self,cursor_details, bitmap, row_details):

        
        # _horizontal_space = ( self.resolution[0]  -  (cursor_details[0]+bitmap.width) ) < self.horizontal_margin
        
        # if(_horizontal_space):
        #     cursor_details[0] = self.horizontal_margin            
        #     cursor_details[1] = cursor_details[1] + (row_details[0]) + self.vertical_margin
        #     row_details[0] = 0

        if(bitmap.buffer == None or bitmap.rows == 0 or bitmap.width == 0):
            return True 
        
        row_details[0] = max(row_details[0], bitmap.rows)

        operations = 0
    
        copy_bitmap = np.array(bitmap.buffer, dtype=np.ubyte)

        for i in range(0, bitmap.rows):
            for j in range(0, bitmap.width):
                
                if(((cursor_details[1] + i) * self.resolution[0]) + cursor_details[0] + j > (self.resolution[0] * self.resolution[1])):
                    return False
                if(((bitmap.rows - i - 1) * bitmap.width + j) > (bitmap.rows*bitmap.width)):
                    return True
                
                self.texture_data[((cursor_details[1] + i) * self.resolution[0]) + cursor_details[0] + j] = copy_bitmap[(bitmap.rows - i - 1) * bitmap.width + j]
                
        cursor_details[0] = cursor_details[0] + bitmap.width + self.horizontal_margin

        return True

    def make_atlas(self):

        if ( self.load_font_to_texture() == False ):
            return

        atlas_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, atlas_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, self.resolution[0], self.resolution[1], 0, GL_RED, GL_UNSIGNED_BYTE, self.texture_data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)

        atlas = bitmap_atlas(self.charmap, self.char_ranges, atlas_texture)

        self.state.add_texture_atlas(self.atlas_name, atlas)


    # returns true if opened face successfuly and added the bitmaps to the texture, else return false.
    def load_font_to_texture(self):

        if(self.resolution != None and self.resolution[0] != 0 and self.resolution[1] != 0):
            self.texture_data = (ctypes.c_ubyte * (self.resolution[0] * self.resolution[1]))(0)


        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]

        filepath = current_directory + "\\" + self.font
        
        face = freetype.Face(filepath)

        if(face == None):
            print("Error loading font")
            return False
        
        face.set_char_size( 48*64 )
        

    
        cursor_details = [self.horizontal_margin,self.vertical_margin]
        row_details = [0,0]

        for i in range(len(self.char_ranges)):
            for j in range(self.char_ranges[i][0],self.char_ranges[i][1]):

                face.load_char(j)
                bitmap = face.glyph.bitmap

                # check to see if the cursor is going to overflow

                _horizontal_space = ( self.resolution[0]  -  (cursor_details[0]+bitmap.width) ) < self.horizontal_margin
        
                if(_horizontal_space):
                        cursor_details[0] = self.horizontal_margin            
                        cursor_details[1] = cursor_details[1] + (row_details[0]) + self.vertical_margin
                        row_details[0] = 0

                if(face.glyph.bitmap.width == 0):
                    self.charmap[ j ] = [
                        0,
                        0,
                        0,
                        0,
                        16/self.resolution[0],
                        16/self.resolution[1],
                        (face.glyph.bitmap_left)/self.resolution[0],
                        (face.glyph.bitmap_top-bitmap.rows)/self.resolution[1],
                    ]
                else:
                    self.charmap[ j ] = [
                        cursor_details[0] / self.resolution[0],
                        cursor_details[1] / self.resolution[1],
                        (cursor_details[0] + bitmap.width) / self.resolution[0],
                        (cursor_details[1] + bitmap.rows) / self.resolution[1],
                        bitmap.width/self.resolution[0],
                        bitmap.rows/self.resolution[1],
                        (face.glyph.bitmap_left)/self.resolution[0],
                        (face.glyph.bitmap_top-bitmap.rows)/self.resolution[1],
                    ]

                inserted = self.insert_bitmap(cursor_details, bitmap, row_details)
                
                if(inserted == False):
                    return
                
                

        # freetype.FT_Done_Face(face)
        # freetype.FT_Done_FreeType(freetype)

        return True
        # Loads and activates font face related to the current sent this.font file path.
    
    def load_onto_quad(self, texture_binding_point = 0):


        mesh_data = (ctypes.c_float * 20)( 
            -1.0,-1.0, 0.0,  0.0, 0.0,
            1.0,-1.0, 0.0,   1.0, 0.0,
            1.0, 1.0, 0.0,   1.0, 1.0,
            -1.0, 1.0, 0.0,  0.0, 1.0
        )

        indices = (ctypes.c_uint * 6)(
            0,1,2,
            0,2,3
        )

        #glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        

        atlas_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, atlas_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, self.resolution[0], self.resolution[1], 0, GL_RED, GL_UNSIGNED_BYTE, self.texture_data)
        
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)


        vertex_buffer = 0
        vertex_array = 0
        element_buffer = 0

        vertex_array = glGenVertexArrays(1)
        vertex_buffer = glGenBuffers(1)
        element_buffer = glGenBuffers(1)
        
        glBindVertexArray(vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer)
        
        glBufferData(GL_ARRAY_BUFFER, 20*4, mesh_data, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, 6*4, indices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(0))
        
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 5*4, ctypes.c_void_p(3*4))
        

        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

        vertex_shader = '''
        #version 460 core\n
        layout(location = 0) in vec3 position;\n
        layout(location = 1) in vec2 texcoord;\n
        out vec2 Texcoord;\n
        void main()\n
        {\n
            gl_Position = vec4(position, 1.0);\n
            Texcoord = texcoord;\n
        }\n
        '''

        fragment_shader = '''
        #version 460 core\n
        in vec2 Texcoord;\n
        uniform sampler2D tex;\n
        out vec4 frag_color;
        void main()\n
        {\n
            
            frag_color = vec4(Texcoord,0.0,1.0);\n
            frag_color = vec4(texture(tex, Texcoord).xyz, 1.0);
            //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n
        }\n
        '''


        program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
    
        #glSetInt(program, "tex", texture_binding_point)
        return vertex_array, element_buffer, program, atlas_texture

                
# joanRegular = TextGeometry()
# joanRegular.LoadActiveFont("fonts\\Joan-Regular.ttf")



                

        

