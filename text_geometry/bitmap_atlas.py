import freetype
import os
import sys
import ctypes
import numpy as np

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *


class bitmap_atlas:
    charmap = None
    char_ranges = None
    atlas_texture = None

    def __init__(self, charmap, char_ranges, atlas_texture):
        self.charmap = charmap
        self.char_ranges = char_ranges
        self.atlas_texture = atlas_texture



class bitmap_atlas_loader:
    char_ranges = [[32,126]]
    chars_loaded = 0
    charmap = {}
    texture_data = None

    def __init__(self, font, resolution, horizontal_margin, vertical_margin):

        self.font = font
        self.resolution = resolution
        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

        return
    
    def insert_bitmap(self,cursor_details, bitmap, row_details):

        
        _horizontal_space = ( self.resolution[0]  -  (cursor_details[0]+bitmap.width) ) < self.horizontal_margin
        
        if(_horizontal_space):
            cursor_details[0] = self.horizontal_margin            
            cursor_details[1] = cursor_details[1] + (row_details[0]) + self.vertical_margin
            row_details[0] = 0

        if(bitmap.buffer == None or bitmap.rows == 0 or bitmap.width == 0):
            return True 
        
        row_details[0] = max(row_details[0], bitmap.rows)

        operations = 0
    
        copy_bitmap = np.array(bitmap.buffer, dtype=np.ubyte)

        for i in range(0, bitmap.rows):
            for j in range(0,bitmap.width):
                
                if(((cursor_details[1] + i) * self.resolution[0]) + cursor_details[0] + j > (self.resolution[0] * self.resolution[1])):
                    return False
                if(((bitmap.rows - i - 1) * bitmap.width + j) > (bitmap.rows*bitmap.width)):
                    return True
                
                self.texture_data[((cursor_details[1] + i) * self.resolution[0]) + cursor_details[0] + j] = copy_bitmap[(bitmap.rows - i - 1) * bitmap.width + j]
                
        cursor_details[0] = cursor_details[0] + bitmap.width + self.horizontal_margin

        return True

    def make_atlas(self, state, name):

        self.LoadActiveFont()
        atlas_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, atlas_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RED, self.resolution[0], self.resolution[1], 0, GL_RED, GL_UNSIGNED_BYTE, self.texture_data)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glBindTexture(GL_TEXTURE_2D, 0)

        state.texture_atlases[name] = [bitmap_atlas(self.charmap, self.char_ranges, atlas_texture), state.used_texture_units]

        state.used_texture_units = state.used_texture_units + 1

        return bitmap_atlas(self.charmap, self.char_ranges, atlas_texture)

    def LoadActiveFont(self):
        if(self.resolution != None and self.resolution[0] != 0 and self.resolution[1] != 0):
            #self.texture_data = [0] * (self.resolution[0] * self.resolution[1])
            self.texture_data = (ctypes.c_ubyte * (self.resolution[0] * self.resolution[1]))(0)
            #self.texture_data = np.array([0] * (self.resolution[0] * self.resolution[1]), dtype=np.ubyte)
            #self.texture_data = np.random.randint(0,255, (self.resolution[0], self.resolution[1],4), dtype=np.ubyte)

        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]

        filepath = current_directory + "\\" + self.font
        
        face = freetype.Face(filepath)

        if(face == None):
            print("Error loading font")
            return
        
        face.set_char_size( 48*64 )

        cursor_details = [self.horizontal_margin,self.vertical_margin]
        row_details = [0,0]

        for i in range(len(self.char_ranges)):
            for j in range(self.char_ranges[i][0],self.char_ranges[i][1]):

                face.load_char(j)
                bitmap = face.glyph.bitmap

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
        void main()\n
        {\n
            gl_FragColor = texture(tex, Texcoord);\n
            //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n
        }\n
        '''


        program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
    
        #glSetInt(program, "tex", texture_binding_point)
        return vertex_array, element_buffer, program, atlas_texture

                





# joanRegular = TextGeometry()
# joanRegular.LoadActiveFont("fonts\\Joan-Regular.ttf")



                

        

