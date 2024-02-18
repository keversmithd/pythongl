# Assuming the script is in a different directory
import sys
import os

from collections import deque

from ..shaders.PyGLHelper import *

class DynamicTextVertexBuffer:
    #            vec3,vec3,vec3,vec3
    # layout = (position,orientation,color,char_index,scalex,scaley)

    char_buffer = []
    char_buffer_index = 0
    available_slots = []

    char_attributes_size = 48
    char_attributes_float_size = 12

    #queue of buffer sub updates
    sub_buffer_update_queue = []

    parameter_map = {
        "character":0,
        "position":1,
        "orientation":4,
        "color":7,
        "scale":10
    }

    def __init__():
        return
    
    def replace_char(self,char_id,char_index,position,orientation,color,scale):
        char_id_index = char_id*self.char_attributes_float_size

        self.char_buffer[char_id_index] = char_index
        self.char_buffer[char_id_index+1] = position[0]
        self.char_buffer[char_id_index+2] = position[1]
        self.char_buffer[char_id_index+3] = position[2]
        self.char_buffer[char_id_index+4] = orientation[0]
        self.char_buffer[char_id_index+5] = orientation[1]
        self.char_buffer[char_id_index+6] = orientation[2]
        self.char_buffer[char_id_index+7] = color[0]
        self.char_buffer[char_id_index+8] = color[1]
        self.char_buffer[char_id_index+9] = color[2]
        self.char_buffer[char_id_index+10] = scale[0]
        self.char_buffer[char_id_index+11] = scale[1]

    #Returns ID or tail of inserted character inside of the buffer.
    #If returns 1, then return 48, s

    def add_char(self,char_index,position,orientation,color,scale):

        if(len(self.available_slots) > 0):
            self.replace_char(self.available_slots.pop(),char_index,position,orientation,color,scale)


        self.char_buffer.append(float(char_index))
        self.char_buffer.append(float(position[0]))
        self.char_buffer.append(float(position[1]))
        self.char_buffer.append(float(position[2]))
        self.char_buffer.append(float(orientation[0]))
        self.char_buffer.append(float(orientation[1]))
        self.char_buffer.append(float(orientation[2]))
        self.char_buffer.append(float(color[0]))
        self.char_buffer.append(float(color[1]))
        self.char_buffer.append(float(color[2]))
        self.char_buffer.append(float(scale[0]))
        self.char_buffer.append(float(scale[1]))

        char_id = char_buffer_index

        char_buffer_index += 1

        return char_id
    
    def remove_char(self,char_id):
        self.char_buffer[char_id*(self.char_attributes_float_size)] = 0
        self.available_slots.append(char_id)

    #Updates a single buffer in the char using glBufferSubUpdate
    def update_buffer_char(self,char_id):
        char_byte_start = char_id*self.char_attributes_size
        char_byte_finish = char_byte_start+self.char_attributes_size



     
class DynamicTextRenderer:

    program = 0 
    DynamicTextBuffer = None

    VertexArray = 0
    VertexBuffer = 0

    def __init__(self):
      self.program = CreateProgram(["text_geometry\\dyn_text.vs", "text_geometry\\dyn_text.gs", "text_geometry\\dyn_text.fs"], [GL_VERTEX_SHADER, GL_GEOMETRY_SHADER, GL_FRAGMENT_SHADER])
    
    
    def CollectBufferUpdate(self):

        sub_collections = []
        


    def SetupBuffers(self):
        self.VertexArray = glGenVertexArrays(1)
        glBindVertexArray(self.VertexArray)
        self.VertexBuffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, self.DynamicTextBuffer.char_buffer_index*self.DynamicTextBuffer.char_attributes_size, self.DynamicTextBuffer.char_buffer, GL_DYNAMIC_DRAW)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), None)
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)

        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(6 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)

        glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(GLfloat), ctypes.c_void_p(9 * sizeof(GLfloat)))
        glEnableVertexAttribArray(3)

        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindVertexArray(0)
    
    def UpdateBuffer(self):
        glBindVertexArray(self.VertexArray)
        glBindBuffer(GL_ARRAY_BUFFER, self.VertexBuffer)
        glBufferData(GL_ARRAY_BUFFER, self.DynamicTextBuffer.char_buffer_index*self.DynamicTextBuffer.char_attributes_size, self.DynamicTextBuffer.char_buffer, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER,0)
        glBindVertexArray(0)
        
    def Draw(self):
        glBindVertexArray(self.VertexArray)
        glDrawArrays(GL_POINT,0,self.DynamicTextBuffer.char_buffer_index)