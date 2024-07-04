import numpy as np
import os
import sys
import ctypes

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *


class InterleavedElementBuffer:

    def __init__(self, map=None):
        self.data = None

        self.format_map = {
            "position": 3,
            "normal": 3,
            "uv": 2,
        }
        self.offset_map = {

        }

        # Define the total size of a vertex unit
        self.vertex_size = 0

        # Define the tail of the current push
        self.tail = 0
        self.subtail = 0

        # define the elements array
        self.elements = None
        self.elements_index = 0

        # define the index slot
        self.index_slot = 0

        # define the range of buffers
        self.vertex_array = 0
        self.vertex_buffer = 0
        self.element_buffer = 0


        # Sets map if map is given
        if ( map != None ):
            self.set_map(map)
    
    #  Set the format map of the interleaved attributes.
    def set_map(self, map):
        self.format_map = map
        return

    # Allocate using the map.
    def allocate(self, number_vertices):

        data_count = 0
        offset_listing = 0
        for k,v in self.format_map.items():
            self.offset_map[k] = offset_listing
            offset_listing += v
            data_count += number_vertices*v
            self.vertex_size += v

        self.data = np.zeros(data_count, dtype=np.float32)

        
        self.elements = np.zeros(number_vertices+(2*number_vertices*3), dtype=np.uint32)
    # Default push

    def push(self, key, value):

        if key in self.offset_map and len(value) >= self.format_map[key]:

            # If the current sub tail exceeds the vertex size
            offset = self.offset_map[key]
            length = self.format_map[key]

            # Increase sub tail by the current attribute length
            self.subtail += length

            for i in range(0,length):
                self.data[(self.tail*self.vertex_size) + offset + i] = value[i]

            if self.subtail == self.vertex_size:
                self.subtail = 0
                self.tail += 1
    
    # Push all | push entire interleaved attribute.
    def push_all(self, value):
        for i in range(0, self.vertex_size):
            self.data[i] = value[i]
        self.tail += 1

    # Push element
    def push_index(self, shape, increment):

        # specify base index
        for s in shape:
            self.elements[(self.elements_index)] = self.index_slot + s
            self.elements_index += 1

        self.index_slot += increment

        return
    
    # Push elements
    def sync_buffers(self):
        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)

        # Then bind the vertex array
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.tail*self.vertex_size*4, self.data, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elements_index*4, self.elements, GL_DYNAMIC_DRAW)

        # Set up current index of the enable attrib array
        current_attrib = 0
        current_attrib_pointer = 0
        for k,v in self.format_map.items():
            glEnableVertexAttribArray(current_attrib)
            glVertexAttribPointer(current_attrib, v, GL_FLOAT, GL_FALSE, self.vertex_size*4, ctypes.c_void_p(current_attrib_pointer*4))
            current_attrib += 1
            current_attrib_pointer += v

    # binds the vertex array and the element buffer
    def bind_for_draw(self):

        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)

    

# Seperate attributes
class ElementBuffer:

    def __init__(self, map=None):

        self.attributes = {}
        self.elements = None
        self.elements_index = 0
        self.index_slot = 0

        # store the offset map
        self.offset_map = {
            
        }

        # size in floats per vertex
        self.vertex_size = 0

        # size of the current attribution
        self.subtail = 0
        self.tail = 0


        return

    def set_map(map):

        # for key value pairs in map
        for k,v in map.items():
            self.offset_map[k] = self.vertex_size
            self.attributes[k] = {data: None, index: 0, stride: v}
            self.vertex_size += v

    def allocate(self, number_vertices):
        
        # attributes
        for attribute in self.attributes:
            attribute.data = np.zeros(attribute.stride*number_vertices, dtype=np.float32)

        self.elements = np.zeros(number_vertices+(2*number_vertices*3), dtype=np.uint32)   

    def push(self, key, value):

        if key in self.attributes:

            attribute = self.attributes[key]
            # If the current sub tail exceeds the vertex size
            offset = self.offset_map[key]
            length = attribute.stride

            # Increase sub tail by the current attribute length
            self.subtail += length

            for i in range(0,length):
                self.data[(self.tail*self.vertex_size) + offset + i] = value[i]

            if self.subtail == self.vertex_size:
                self.subtail = 0
                self.tail += 1

    def push_index(self, shape, increment):

        # specify base index
        for s in shape:
            self.elements[(self.elements_index)] = self.index_slot + s
            self.elements_index += 1

        self.index_slot += increment

        return
    
    # Push elements
    def sync_buffers(self):
        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)

        # Then bind the vertex array
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, self.tail*self.vertex_size*4, self.data, GL_DYNAMIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.elements_index*4, self.elements, GL_DYNAMIC_DRAW)

        # Set up current index of the enable attrib array
        current_attrib = 0
        current_attrib_pointer = 0
        for k,v in self.format_map.items():
            glEnableVertexAttribArray(current_attrib)
            glVertexAttribPointer(current_attrib, v, GL_FLOAT, GL_FALSE, self.vertex_size*4, ctypes.c_void_p(current_attrib_pointer))
            current_attrib += 1
            current_attrib_pointer += v

    # binds the vertex array and the element buffer
    def bind_for_draw(self):

        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)