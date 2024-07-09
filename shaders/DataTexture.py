
import numpy as np
import os
import sys
import ctypes

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

# texture options
# {
#   dimension: 1D | 2D | 3D
#   format: GL_RED | GL_RGB
#   wrap: ( count for both )
#   filter: ( count for both )
#   wrap_s
#   wrap_t
#   min_filter
#   mag_filter
#   dimensions
# }

# Array format is an np.zeroes data array
# 
#
class DataTexture :

    def __init__(self, state, width, height, data, texture_options):

        # establish the variables 
        self.width = width
        self.height = height

    
        if ( texture_options == None ):
            self.texture_options = {
                "dimensions" : "2D",
                "format"  : GL_RED,
                "internal_format" : GL_RED,
                "wrap_s" : GL_CLAMP_TO_EDGE,
                "wrap_t" : GL_CLAMP_TO_EDGE,
                "min_filter" : GL_LINEAR,
                "mag_filter" : GL_LINEAR,
                "type" : GL_UNSIGNED_BYTE
            }
        else:
            self.finish_texture_options(texture_options)

        # just a pixel stride map
        self.pixel_stride_map = {
            GL_RED : 1,
            GL_RGB : 3,
            GL_RGBA: 4,
        }

        # If the data doesn't exist it initalizes the data, and sets the tail for the data at 0, so that it can be pushed, other wise it uses the data array and sets the tail and size.
        if ( data == None ):

            if ( texture_options["type"] == GL_UNSIGNED_BYTE ):
                self.data = np.zeros( max(1,width)*max(1, height), dtype=np.uint8)
            if ( texture_options["type"] == GL_FLOAT ):
                self.data = np.zeros( max(1,width)*max(1,height), dtype=np.float32)

            self.data_capacity = max(1,width)*max(1,height)
            self.data_tail = 0

        else:
            # set the data
            self.data = data
            # set the capacity in terms of dtype elements of the array
            self.data_capacity = data.size 
            self.data_tail = data.size

        # A region indicator for where the data needs to be updated to the gpu.
        self.update_region_begin = 0
        self.update_region_end = 0
        self.needs_update = False
        self.full_update_needed = False

        # Establish the texture unit and texture obj
        self.texture_unit = state.add_texture_unit()
        self.make_texture()

        # in the future add a section for disposed texture_pixels, in which when pushing

    def finish_texture_options(self, texture_options):

        if "dimension" not in texture_options:
            texture_options["dimension"] = "1D"

        if "wrap" in texture_options:
            texture_options["wrap_t"] = texture_options["wrap"]
            texture_options["wrap_s"] = texture_options["wrap"]
        else:

            if ( "wrap_t" not in texture_options ):
                texture_options["wrap_t"] = GL_CLAMP_TO_BORDER
            if ( "wrap_s" not in texture_options ):
                texture_options["wrap_s"] = GL_CLAMP_TO_BORDER
        
        if "filter" in texture_options:
            texture_options["min_filter"] = texture_options["filter"]
            texture_options["mag_filter"] = texture_options["filter"]
        else:

            if ( "min_filter" not in texture_options ):
                texture_options["min_filter"] = GL_LINEAR
            if ( "mag_filter" not in texture_options ):
                texture_options["mag_filter"] = GL_LINEAR

        if "format" not in texture_options:
            texture_options["format"] = GL_RED
        
        if "internal_format" not in texture_options:
            texture_options["internal_format"] = GL_RED

        if "type" not in texture_options:
            texture_options["type"] = GL_UNSIGNED_BYTE

        if ( texture_options["dimension"] == "1D" ):
            self.texture_bind = GL_TEXTURE_1D
        elif ( texture_options["dimension"] == "2D"):
            self.texture_bind = GL_TEXTURE_2D

        self.texture_options = texture_options

    # initially create the texture.
    def make_texture(self):

        self.texture_obj = glGenTextures(1)
        
        if ( self.texture_options["dimension"] == "1D" ):
            glBindTexture(GL_TEXTURE_1D, self.texture_obj)
            glTexImage1D(GL_TEXTURE_1D, 0, self.texture_options["internal_format"], self.width, 0, self.texture_options["format"], self.texture_options["type"], self.data)
            
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, self.texture_options["wrap_s"])
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, self.texture_options["wrap_t"])
            
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, self.texture_options["min_filter"])
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, self.texture_options["mag_filter"])

            glBindTexture(GL_TEXTURE_1D, 0)
        if ( self.texture_options["dimension"] == "2D" ):
            glBindTexture(GL_TEXTURE_2D, self.texture_obj)
            glTexImage2D(GL_TEXTURE_2D, 0, self.texture_option["internal_format"], self.width, self.height, 0, self.texture_option["format"], self.texture_option["type"], self.data)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.texture_option["wrap_s"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.texture_option["wrap_t"])
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.texture_option["min_filter"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.texture_option["mag_filter"])

            glBindTexture(GL_TEXTURE_2D, 0)

    # then resize the texture then multiply by two.
    def resize(self):

        if ( self.texture_options["dimension"] == "1D" ):
            self.data = np.resize(self.data, (self.width*2))
            self.data_capacity = ( self.width*2)
            self.width = self.width*2
            
            # Set indicator that full_update needed
            self.full_update_needed = True

        if ( self.texture_options["dimension"] == "2D" ):
            self.data = np.resize(self.data, (self.width*2)*(self.height*2))
            self.width = self.width*2
            self.height = self.height*2
            self.capacity = ( self.width*2)*(self.height*2)

            # Set indicator that full_update needed
            self.full_update_needed = True
    
    # push value to the texture data and increment region 
    def push_pixel(self, value):
        # Resize the array and texture GPU data 
        if ( self.data_tail + 1 > self.data_capacity ):
            self.resize()
        
        self.data[self.data_tail] = value
        self.data_tail += 1
        self.update_region_end += 1
        self.needs_update = True
    
    # push a vector against the tail of the data.
    def push_vector(self, value):

        # return head of the current vector object in the texture
        data_tail = self.data_tail

        if ( len(value) <= 0 ):
            return

        # Resize the array and texture GPU data 
        if ( self.data_tail + len(value) > self.data_capacity ):
            self.resize()
        
        for i in range(0, len(value)):
            self.data[self.data_tail] = value[i]
            self.data_tail += 1

        self.update_region_end += int ( (len(value)) )
        self.needs_update = True

        return data_tail

    # updates region depending on updated_vector locations
    def update_region_bounds(self, tail, length):

        # here since using multitudes of tex image would probably be more costly, just min max the region instead
        if ( self.update_region_begin == self.update_region_end ):
            self.update_region_begin = tail
            self.update_region_end = tail+length
        else:
            if ( tail < self.update_region_begin ):
                self.update_region_begin = tail
            if ( tail+length > self.update_region_end ):
                self.update_region_end = tail+length

    # update a specific vector location
    def update_vector(self, value, tail):
        
        if ( len(value) <= 0 ):
            return

        # Resize the array and texture GPU data 
        if ( tail > self.data_capacity ):
            return
        
        for i in range(0, len(value)):
            self.data[tail+i] = value[i]

        self.update_region_bounds(tail, len(value))
        self.needs_update = True

    # Updates texture region from update_region_begin to update_region end, updates the update_region_begin to be at the end
    def update_region(self):

        if ( self.update_region_end <= self.update_region_begin ):
            return

        if ( self.texture_options["dimension"] == "1D" ):
            glBindTexture(GL_TEXTURE_1D, self.texture_obj)

            data_view = memoryview(self.data)[self.update_region_begin:self.update_region_end]

            pixel_stride = self.pixel_stride_map[ self.texture_options["format"] ]
            pixel_width = int((self.update_region_end-self.update_region_begin)/pixel_stride)
            pixel_offset = int((self.update_region_begin)/pixel_stride)
            glTexSubImage1D(GL_TEXTURE_1D, 0, pixel_offset, pixel_width, self.texture_options["format"], self.texture_options["type"], data_view)
            glBindTexture(GL_TEXTURE_1D, 0)


            self.update_region_begin = self.update_region_end

        if ( self.texture_options["dimension"] == "2D" ):
            glBindTexture(GL_TEXTURE_2D, self.texture_obj)
            data_view = memoryview(self.data)[self.update_region_begin:self.update_region_end]
            
            # need to decompose the begin and end into the texture region.
            yoffset = int(self.update_region_begin / self.width)
            xoffset = self.update_region_begin % self.width
            width = (self.width - xoffset)
            height = (self.update_region_end - self.update_region_begin) / self.width
            glTexSubImage2D(GL_TEXTURE_2D, 0, xoffset, yoffset, width, height, self.texture_options["format"], self.texture_options["type"], data_view)
            glBindTexture(GL_TEXTURE_2D, 0)

            self.update_region_begin = self.update_region_end

    # Updates entire texture data point not by region 
    def full_update(self):
        if ( self.texture_options["dimension"] == "1D" ):
            glBindTexture(GL_TEXTURE_1D, self.texture_obj)
            glTexImage1D(GL_TEXTURE_1D, 0, self.texture_options["internal_format"], self.width, 0, self.texture_options["format"], self.texture_options["type"], self.data)
            
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_S, self.texture_options["wrap_s"])
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_WRAP_T, self.texture_options["wrap_t"])
            
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MIN_FILTER, self.texture_options["min_filter"])
            glTexParameteri(GL_TEXTURE_1D, GL_TEXTURE_MAG_FILTER, self.texture_options["mag_filter"])

            glBindTexture(GL_TEXTURE_1D, 0)
            self.update_region_begin = self.update_region_end
        if ( self.texture_options["dimension"] == "2D" ):
            glBindTexture(GL_TEXTURE_2D, self.texture_obj)
            glTexImage2D(GL_TEXTURE_2D, 0, self.texture_option["format"], self.width, self.height, 0, self.texture_option["format"], self.texture_option["type"], self.data)
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.texture_option["wrap_s"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.texture_option["wrap_t"])
            
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.texture_option["min_filter"])
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.texture_option["mag_filter"])

            glBindTexture(GL_TEXTURE_2D, 0)
            self.update_region_begin = self.update_region_end

    def update(self):

        if ( self.full_update_needed == True ):
            self.full_update()
            self.full_update_needed = False
            self.needs_update = False
        if ( self.needs_update == True ):
            self.update_region()
            self.needs_update = False
        
        
        return



