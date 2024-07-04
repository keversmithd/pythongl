import freetype
import os
import sys
import ctypes
import numpy as np
import copy
from collections import deque

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

from data_structures.box_query_grid.box_query_grid import *
from math_structures.bezier_curves.c_bezier import *
from math_structures.bezier_curves.q_bezier import * 
from math_structures.bezier_curves.vec2 import *

from data_structures.quadtree.quadtree import *
# import threading since this takes so many efforts
import threading

    

class sdf_atlas_loader:
    char_ranges = [[33,44]]
    chars_loaded = 0
    charmap = {}
    texture_data = None

    def __init__(self, font, resolution, horizontal_margin, vertical_margin):

        self.font = font
        self.resolution = resolution
        self.horizontal_margin = horizontal_margin
        self.vertical_margin = vertical_margin

        return
    
    # subroutine determines distance between two pixel coordinates in pixels
    def coordinate_distance(self, pixelA, pixelB):
        a = abs(pixelB[0] - pixelA[0])
        b = abs(pixelB[1] - pixelA[1])

        return a+b
        
    # subroutine for getting current index into the bitmap
    def bitmap_index(self, pixel_location, width):

        return ( pixel_location[1] * width ) + pixel_location[0]

    # will calculate and return the signed distance to a bitmap value of opposite state
    def calculate_sdf_bfs(self, bitmap_pixel_location, bitmap_buffer, bitmap_width, bitmap_height, operation_count):

        # Define the true limit for a pixel value between 0 and 255
        truth_limit = 0

        # Gather the bitmap pixel index
        bitmap_pixel_index = self.bitmap_index( bitmap_pixel_location, bitmap_width )

        # Get the initial pixel state of this location
        pixel_state = ( bitmap_buffer[ bitmap_pixel_index ] > truth_limit )

        Q = deque()
        Q.append(bitmap_pixel_location)
        # Add the inital pixel location to the queue

        # Where do we stop, we must handle everything already in the queue but once we encounter atleast one of opposite state, then we stop appending, in the next cycle
        found_flag = False
        append_flag = True

        # We are going to need the maximum distance, and the minimum distance.
        minimum_distance = 12838
        
        #visited array
        visited = {}

        max_iter = bitmap_width*bitmap_height

        it = 0

        # While the queue is not empty
        while ( len(Q) > 0 and it < max_iter ):
            # Pop the current pixel location
            current_pixel = Q.popleft()

            operation_count[0] += 1

            visited[f"{current_pixel[0]},{current_pixel[1]}"] = 1

            # Add the neigbors of the cell
            if ( current_pixel[0]-1 >= 0 and f"{current_pixel[0]-1},{current_pixel[1]}" not in visited):

                # Set this node as visited so it is not added to the queue again.
                visited[f"{current_pixel[0]-1},{current_pixel[1]}"] = 1

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]-1, current_pixel[1]]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

                    # set the found flag so that, the append flag is disabled after this neighbor step.
                    found_flag = True

                # If the texel is of opposite state, then log its distance.
                if ( append_flag == True ):
                    Q.append( neighbor_coordinate )

            
            # Add the neigbors of the cell
            if ( current_pixel[1]-1 >= 0 and f"{current_pixel[0]},{current_pixel[1]-1}" not in visited):

                # Set this node as visited so it is not added to the queue again.
                visited[f"{current_pixel[0]},{current_pixel[1]-1}"] = 1

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0], current_pixel[1]-1]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

                    # set the found flag so that, the append flag is disabled after this neighbor step.
                    found_flag = True

                # If the texel is of opposite state, then log its distance.
                if ( append_flag == True ):
                    Q.append( neighbor_coordinate )

            # Add the neigbors of the cell
            if ( current_pixel[0]+1 < bitmap_width-1 and f"{current_pixel[0]+1},{current_pixel[1]}" not in visited):

                # Set this node as visited so it is not added to the queue again.
                visited[f"{current_pixel[0]+1},{current_pixel[1]}"] = 1

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]+1, current_pixel[1]]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

                    # set the found flag so that, the append flag is disabled after this neighbor step.
                    found_flag = True

                # If the texel is of opposite state, then log its distance.
                if ( append_flag == True ):
                    Q.append( neighbor_coordinate )

            # Add the neigbors of the cell
            if ( current_pixel[1]+1 < bitmap_height-1 and f"{current_pixel[0]},{current_pixel[1]+1}" not in visited):

                # Set this node as visited so it is not added to the queue again.
                visited[f"{current_pixel[0]},{current_pixel[1]+1}"] = 1

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0], current_pixel[1]+1]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

                    # set the found flag so that, the append flag is disabled after this neighbor step.
                    found_flag = True

                # If the texel is of opposite state, then log its distance.
                if ( append_flag == True ):
                    Q.append( neighbor_coordinate )

            if found_flag == True:
                append_flag = False

            it += 1


        #print(it, max_iter)

        return minimum_distance

    def calculate_sdf_kernel(self, bitmap_pixel_location, bitmap_buffer, bitmap_width, bitmap_height):
        # Define the true limit for a pixel value between 0 and 255
        truth_limit = 0

        # Gather the bitmap pixel index
        bitmap_pixel_index = self.bitmap_index( bitmap_pixel_location, bitmap_width )

        # Get the initial pixel state of this location
        pixel_state = ( bitmap_buffer[ bitmap_pixel_index ] > truth_limit )

        # Where do we stop, we must handle everything already in the queue but once we encounter atleast one of opposite state, then we stop appending, in the next cycle
        found_flag = False
        append_flag = True

        current_pixel = bitmap_pixel_location

        kernel_size = 2

        minimum_distance = 255

        for i in range(1, kernel_size):

            # Add the neigbors of the cell
            if ( current_pixel[0]-(1*i) >= 0):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]-(1*i), current_pixel[1]]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[0]+(1*i) < bitmap_width):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]+(1*i), current_pixel[1]]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[1]-(1*i) >= 0):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0], current_pixel[1]-(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[1]+(1*i) < bitmap_height ):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0], current_pixel[1]+(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[0]-(1*i) >= 0 and current_pixel[1]-(1*i) >= 0):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]-(1*i), current_pixel[1]-(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[0]-(1*i) >= 0 and current_pixel[1]+(1*i) < bitmap_height):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]-(1*i), current_pixel[1]+(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )


            # Add the neigbors of the cell
            if ( current_pixel[0]+(1*i) < bitmap_width and current_pixel[1]-(1*i) >= 0):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]+(1*i), current_pixel[1]-(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

            # Add the neigbors of the cell
            if ( current_pixel[0]+(1*i) < bitmap_width and current_pixel[1]+(1*i) < bitmap_height):

                # Calculate the coordinate of the neighbor cell.
                neighbor_coordinate = [current_pixel[0]+(1*i), current_pixel[1]+(1*i)]

                bitmap_index = self.bitmap_index(neighbor_coordinate, bitmap_width)

                # calculate the adjacent pixel state
                adjacent_pixel_state = ( bitmap_buffer[ bitmap_index ] > truth_limit )

                if ( adjacent_pixel_state != pixel_state ):
                    coordinate_distance = self.coordinate_distance(bitmap_pixel_location, neighbor_coordinate)
                    minimum_distance = min( minimum_distance,  coordinate_distance )

        
        return minimum_distance

    def insert_sdf_char(self):

        bitmap_width = self.operation_face.glyph.bitmap.width
        bitmap_height = self.operation_face.glyph.bitmap.rows
        bitmap_buffer = self.operation_face.glyph.bitmap.buffer

        # Find the normalized width and scale in relation to the max
        norm_width = self.bitmap_width/self.font_face_resolution
        norm_height = self.bitmap_height/self.font_face_resolution

        # Find the respective width and height of the target char unrounded in order to get back
        target_unrounded_width = norm_width * self.low_resolution_char_size
        target_unrounded_height = norm_height * self.low_resolution_char_size

        # Find the scale up factor the multiples of size difference from lower to higher | both should be in powers of two.
        scale_up_factor = self.font_face_resolution/self.low_resolution_char_size

        # Store the min and max distances in pixel space, so that the results can be normalized at the end?
        max_distance = 1

        operation_count = [0]

        for j in range(0, round(target_unrounded_height) ):
            for i in range(0, round(target_unrounded_width)):
                # Texutre pixel location within the texture
                texture_pixel_location = [self.cursor[0]+i, self.cursor[1]+j ]

                # Find the unrounded pixel coorelation in the bitmap, should always be withought remainder
                bitmap_pixel_location = [ int ( ( i/round(target_unrounded_width))*bitmap_width ) , int ( ( (round(target_unrounded_height)-j-1)/round(target_unrounded_height))*bitmap_height ) ]

                # Calculate the signed distance between this texel and the closest texel of opposite value.abs
                distance = self.calculate_sdf_bfs(bitmap_pixel_location, bitmap_buffer, bitmap_width, bitmap_height, operation_count)
                #distance = self.calculate_sdf_kernel(bitmap_pixel_location, bitmap_buffer, bitmap_width, bitmap_height)


                
                max_distance = max(max_distance, distance)
                #print(distance)

                # Calculate min and max distances
                

                # Then write the value to the texture location.
                #self.texture_data[ ( (self.cursor[1]+texture_pixel_location[1])*self.resolution[0] ) + (self.cursor[0] + texture_pixel_location[0] ) ] = distance
                #self.texture_data[ ( (texture_pixel_location[1])*self.resolution[0] ) + (texture_pixel_location[0] ) ] = 255

                val = bitmap_buffer[
                    bitmap_pixel_location[1]*bitmap_width + bitmap_pixel_location[0]

                ]

                self.texture_data[ ( (texture_pixel_location[1])*self.resolution[0] ) + (texture_pixel_location[0] ) ] = int( (distance/(bitmap_height)) * 255 )


        print(operation_count)
        # if ( max_distance != 0 ):
        #     for i in range(0, round(target_unrounded_width)):
        #         for j in range(0, round(target_unrounded_height)):
        #             # Texutre pixel location within the texture
        #             texture_pixel_location = [ self.cursor[0]+i, self.cursor[1]+j ]
                
        #             value = self.texture_data[ ( (texture_pixel_location[1])*self.resolution[0] ) + (texture_pixel_location[0]) ]

        #             self.texture_data[ ( (texture_pixel_location[1])*self.resolution[0] ) + (texture_pixel_location[0]) ] = int (  ( ((value)/max_distance) ) * 255 )
        
        if ( self.cursor[0] + round(target_unrounded_width) >= self.resolution[0] ):
            self.cursor[0] = 0
            self.cursor[1] += self.low_resolution_char_size
        else:  
            self.cursor[0] += round(target_unrounded_width)
        
    def allocate_texture_data(self, low_resolution_char_size, number_of_chars):
        # This needs to allocate a texture large enough to handle the number of characters being
        # transfered into bitmap location
        width = int(number_of_chars*low_resolution_char_size/2)
        height = int(number_of_chars*low_resolution_char_size/2)

        self.resolution[0] = width
        self.resolution[1] = height

        self.texture_data = (ctypes.c_ubyte * (width * height))(0)

    def activate_font_face(self, char_resolution):

        # Append the font file path to the working directory.
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]
        filepath = current_directory + "\\" + self.font

        self.operation_face = freetype.Face(filepath)

        if(self.operation_face == None):
            print("Error loading font")
            return

        # The character widths and heights are specified in 1/64 of points, and sets resolution for DPI specific usage set_char_size
        # Set pixel sizes
        self.operation_face.set_pixel_sizes(char_resolution, char_resolution)

        return

    # Creates texture data with SDFs
    def make_sdf_atlas_grid(self):

        desired_resolution = 32

        char_resolution = 64

        self.allocate_texture_data(desired_resolution,10)

        # Append the font file path to the working directory.
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]
        filepath = current_directory + "\\" + self.font

        face = freetype.Face(filepath)

        # The character widths and heights are specified in 1/64 of points, and sets resolution for DPI specific usage set_char_size
        # Set pixel sizes
        face.set_pixel_sizes(char_resolution, char_resolution)
        
        self.cursor=[0,0]

        # select vertical padding amount or could be adjusted to simulate the amount of horizontal padding.
        vertical_padding = 0.2

        for c in range(70, 77):
            # load the test char
            face.load_char(c, flags=freetype.FT_LOAD_RENDER )

            # get the outline
            outline = face.glyph.outline

            bbox = outline.get_bbox()
            # create the box query grid
            query_grid = sdf_grid( [0,0,1,1], 10 )

            # store the last end point of the bezier curve
            last_end_point = 0
            first_end_point = 0
            # iterate through the outline contours
            
            for i in range(0, outline.n_contours):

                contour_end_point = outline.contours[i]
                
                curve_range = (last_end_point, contour_end_point)
                first_end_point = last_end_point
                # store the last point bay and last curve type.

                # store points so that once the curve type is determined
                point_bay = []
                
                # if 0, then quadratic if 1 then 
                curve_type = 0

                # store the end of the last bezier curve inserted
                end_of_last_curve = 0

                for j in range(last_end_point, contour_end_point+1):
                    
                    point = outline.points[j]
                    tag = outline.tags[j]

                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    if ( normalized_point[0] > 1.0 ):
                        normalized_point[0] = 1.0
                    if ( normalized_point[0] < 0):
                        normalized_point[0] = 0
                    if ( normalized_point[1] > 1.0 ):
                        normalized_point[1] = 1.0
                    if ( normalized_point[1] < 0 ):
                        normalized_point[1] = 0


                    # determine if on or off curve.
                    b0 = tag & 0b00000001

                    if ( b0 == 1 ):
                        if ( len(point_bay) >= 2 and curve_type == 0 ):
                            point_bay.append(normalized_point)

                            curve = q_bezier(point_bay[0], point_bay[1], point_bay[2])
                            container = curve.bounding_rectangle()
                            
                            #curve.display()
                            # if last_curve_type == 0 : norm = cross(p1-p0, p3-p2)

                            query_grid.insert_container( container, curve )

                            # create the correct bezier curve object
                            point_bay.clear()

                            end_of_last_curve = normalized_point

                        if ( len(point_bay) >= 3 and curve_type == 1 ):
                            point_bay.append(normalized_point)

                            curve = c_bezier(point_bay[0], point_bay[1], point_bay[2], point_bay[3])
                            container = curve.bounding_rectangle()

                            #curve.display()

                            query_grid.insert_container( container, curve )

                            point_bay.clear()
                            end_of_last_curve = normalized_point

                    # store in the point bay
                    point_bay.append(normalized_point)

                    # if off curve, then check the curve status
                    if ( b0 == 0 ):
                        
                        if ( len(point_bay) > 2 and curve_type == 0 ):
                            
                            curve = q_bezier(point_bay[0], point_bay[1], point_bay[2])
                            #curve.display()
                            container = curve.bounding_rectangle()

                            query_grid.insert_container( container, curve )

                            end_of_last_curve = point_bay[2]
                            point_bay.clear()
                            point_bay.append(normalized_point)

                            
                        if ( len(point_bay) > 3 and curve_type == 1 ):

                            curve = c_bezier(point_bay[0], point_bay[1], point_bay[2], point_bay[3])
                            #curve.display()
                            container = curve.bounding_rectangle()

                            query_grid.insert_container( container, curve )

                            end_of_last_curve = point_bay[2]
                            point_bay.clear()
                            point_bay.append(normalized_point)

                        b1 = tag & 0b00000010
                        curve_type = b1

                last_end_point = contour_end_point+1
                
                if ( len(point_bay) == 2):  
                    
                    point = outline.points[first_end_point]
                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    curve = q_bezier(point_bay[0], point_bay[1], normalized_point)
                    #curve.display()
                    container = curve.bounding_rectangle()
                    query_grid.insert_container( container, curve )
                    point_bay.clear()
                    

                if ( len(point_bay) == 1):

                    point = outline.points[first_end_point]
                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    curve = vec2(point_bay[0], normalized_point)
                    container = curve.bounding_rectangle()
                    query_grid.insert_container( container, curve )
                    point_bay.clear()

            last_distance = -1
            epsilon_limit = 0.1
            #iterate through the desired resolution
            for j in range(0, desired_resolution+1):
                for i in range(0, desired_resolution+1):

                    u = i/desired_resolution
                    v = j/desired_resolution
                    
                    pixel_limit = math.ceil(desired_resolution*vertical_padding/2)

                    in_margin = (j < pixel_limit) or (j > desired_resolution-pixel_limit)

                    #distance = query_grid.query_closest_cell(u,v)
                    distance, inside = query_grid.query_closest_cell(u,v)

                    texture_coordinate = [self.cursor[0] + i, self.cursor[1] + j]

                    if ( inside == True ):
                        self.texture_data[ (texture_coordinate[1] * self.resolution[0]) + texture_coordinate[0] ] = 255
                    else:
                        self.texture_data[ (texture_coordinate[1] * self.resolution[0]) + texture_coordinate[0] ] = int(((1-distance)*0.5)*255)
                    #self.texture_data[ (texture_coordinate[1] * self.resolution[0]) + texture_coordinate[0] ] = int(((distance))*255)
                    #exture_coordinate = [self.cursor[0] + i, self.cursor[1] + j]
                    #self.texture_data[ (texture_coordinate[1] * self.resolution[0]) + texture_coordinate[0] ] = int(((distance-0.5)*-1)*255)
                    last_distance = distance

                place = "left"
                last_distance = -1
            

            if ( self.cursor[0] + desired_resolution > self.resolution[0] ):
                self.cursor[0] = 0
                self.cursor[1] += desired_resolution
            else:
                self.cursor[0] += desired_resolution
            
        #print(iteration_count[0])    

        print("done")


        return

    def make_sdf_atlas_scan(self):

        desired_resolution = 32

        char_resolution = 64

        self.allocate_texture_data(desired_resolution,10)

        
        # Append the font file path to the working directory.
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]
        filepath = current_directory + "\\" + self.font

        face = freetype.Face(filepath)

        # The character widths and heights are specified in 1/64 of points, and sets resolution for DPI specific usage set_char_size
        # Set pixel sizes
        face.set_pixel_sizes(desired_resolution, desired_resolution)

        self.cursor = [0,0]


        for c in range(76, 78):
            # load the test char
            face.load_char(c, flags=freetype.FT_LOAD_RENDER )

            bitmap_width = face.glyph.bitmap.width
            bitmap_height = face.glyph.bitmap.rows
            bitmap = face.glyph.bitmap.buffer

            # surface limit
            surface_limit = 50

            max_distance = 0
            start = 0
            end = 0

            horizontal_margin_width = math.floor( (desired_resolution-bitmap_width)/2 )

            if ( horizontal_margin_width == 0 ):
                horizontal_margin_width = 1

            vertical_margin_height = math.floor ( (desired_resolution-bitmap_height)/2 )

            if ( vertical_margin_height == 0 ):
                vertical_margin_height = 1

            last_bitmap_value = -1

            last_state = ""
            
            # iterate through the bitmap
            for j in range(0, bitmap_height):

                start = 0
                end = 0

                for i in range(0, bitmap_width):
                    
                    bitmap_coordinate = ((bitmap_height-j-1)*bitmap_width) + i
                    bitmap_value = bitmap[bitmap_coordinate]

                    # end is the current pixel in the range and ends at the condition
                    end += 1

                    if ( last_bitmap_value < surface_limit and bitmap_value > surface_limit and last_bitmap_value != -1):
                        # outside to inside

                        if ( start == 0 ):


                            # if the start is zero and it is measuring the top pixel
                            if ( j == 0 ):
                                # then iterate through the top margin\
                                current_distance = 0.0
                                for m in range(0, vertical_margin_height):
                                    total_distance = max_distance+horizontal_margin_width
                                    pixel_distance = 1/(2*total_distance)
                                    current_distance = 0.0
                                    for k in range(0, end+horizontal_margin_width):
                                        texture_index = (((m + self.cursor[1]))*self.resolution[0]) + k + self.cursor[0]
                                        self.texture_data[ texture_index ] = int( current_distance*255 )
                                        current_distance += pixel_distance


                            max_distance += horizontal_margin_width
                            # calculate the distance of one pixel in this range
                            pixel_distance = 1/(2*max_distance+1)
                            current_distance = 0.0
                            for k in range(0, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int( current_distance*255 )
                                current_distance += pixel_distance
                            # then start should pick up at the next pixel
                            start = end
                        else:
                            pixel_distance = 1/(2*max_distance)
                            current_distance = 0.5
                            for k in range(start+horizontal_margin_width, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance -= pixel_distance
                            # then start should pick up at the next pixel
                            start = end
                        
                        max_distance = 0

                    if ( last_bitmap_value > surface_limit and bitmap_value < surface_limit and last_bitmap_value != -1 ):
                        # inside to outside
                        if ( start == 0 ):
                            max_distance += horizontal_margin_width
                            # calculate the distance of one pixel in this range
                            pixel_distance = 1/(2*max_distance)
                            current_distance = 0.5
                            middle = math.floor( ((start)+end)/2 ) 

                            
                            # margin delta
                            margin_distance = 1.0/( 3*horizontal_margin_width )
                            for k in range(0, horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int((k*margin_distance)*255)

                            for k in range(start+horizontal_margin_width+1, middle+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance += pixel_distance
                            
                            for k in range(middle+horizontal_margin_width, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance -= pixel_distance

                        else:
                            pixel_distance = 1/(2*max_distance)
                            current_distance = 0.5
                            middle = math.floor ( (start+end)/2 )

                            for k in range(start+horizontal_margin_width, middle+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance += pixel_distance
                                
                                
                            for k in range(middle+horizontal_margin_width, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance -= pixel_distance

                        # then start should pick up at the next pixel
                        start = end

                        max_distance = 0

                    if ( last_bitmap_value < surface_limit and i == (bitmap_width-1) and last_bitmap_value != -1 ):
                        pixel_distance = 1/(2*max_distance)
                        current_distance = 0.5
                        if ( start == 0 ):
                            for k in range(start+horizontal_margin_width, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                #self.texture_data[ texture_index ] = 0
                            # then start should pick up at the next pixel
                            start = 0
                        else:
                            for k in range(start+horizontal_margin_width, end+horizontal_margin_width):
                                texture_index = (((j + self.cursor[1]) + vertical_margin_height)*self.resolution[0]) + k + self.cursor[0]
                                self.texture_data[ texture_index ] = int(current_distance*255)
                                current_distance -= pixel_distance
                            start = 0

                        max_distance = 0
                            

                    max_distance += 1
                    last_bitmap_value = bitmap_value

            if ( self.cursor[0] + desired_resolution > self.resolution[0] ):
                self.cursor[0] = 0
                self.cursor[1] += desired_resolution
            else:
                self.cursor[0] += desired_resolution

    def make_sdf_atlas_quad(self):

        desired_resolution = 32

        char_resolution = 64

        self.allocate_texture_data(desired_resolution,10)

        # Append the font file path to the working directory.
        current_directory = os.path.dirname(os.path.realpath(__file__))
        current_directory = current_directory.rsplit('\\', 1)[0]
        filepath = current_directory + "\\" + self.font

        face = freetype.Face(filepath)

        # The character widths and heights are specified in 1/64 of points, and sets resolution for DPI specific usage set_char_size
        # Set pixel sizes
        face.set_pixel_sizes(desired_resolution, desired_resolution)
        
        self.cursor=[0,0]

        # select vertical padding amount or could be adjusted to simulate the amount of horizontal padding.
        vertical_padding = 0.2

        for c in range(70, 77):
            # load the test char
            face.load_char(c, flags=freetype.FT_LOAD_RENDER )

            # get the outline
            outline = face.glyph.outline

            bbox = outline.get_bbox()
            # create the box query grid
            query_quad = sdf_quadtree( [0,0,1,1] )

            # store the last end point of the bezier curve
            last_end_point = 0
            first_end_point = 0
            # iterate through the outline contours
            
            for i in range(0, outline.n_contours):

                contour_end_point = outline.contours[i]
                
                curve_range = (last_end_point, contour_end_point)
                first_end_point = last_end_point
                # store the last point bay and last curve type.

                # store points so that once the curve type is determined
                point_bay = []
                
                # if 0, then quadratic if 1 then 
                curve_type = 0

                # store the end of the last bezier curve inserted
                end_of_last_curve = 0

                for j in range(last_end_point, contour_end_point+1):
                    
                    point = outline.points[j]
                    tag = outline.tags[j]

                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    if ( normalized_point[0] > 1.0 ):
                        normalized_point[0] = 1.0
                    if ( normalized_point[0] < 0):
                        normalized_point[0] = 0
                    if ( normalized_point[1] > 1.0 ):
                        normalized_point[1] = 1.0
                    if ( normalized_point[1] < 0 ):
                        normalized_point[1] = 0


                    # determine if on or off curve.
                    b0 = tag & 0b00000001

                    if ( b0 == 1 ):
                        if ( len(point_bay) >= 2 and curve_type == 0 ):
                            point_bay.append(normalized_point)

                            curve = q_bezier(point_bay[0], point_bay[1], point_bay[2])
                            container = curve.bounding_rectangle()
                            
                            #curve.display()
                            # if last_curve_type == 0 : norm = cross(p1-p0, p3-p2)

                            query_quad.insert( container, curve )

                            # create the correct bezier curve object
                            point_bay.clear()

                            end_of_last_curve = normalized_point

                        if ( len(point_bay) >= 3 and curve_type == 1 ):
                            point_bay.append(normalized_point)

                            curve = c_bezier(point_bay[0], point_bay[1], point_bay[2], point_bay[3])
                            container = curve.bounding_rectangle()

                            #curve.display()

                            query_quad.insert( container, curve )

                            point_bay.clear()
                            end_of_last_curve = normalized_point

                    # store in the point bay
                    point_bay.append(normalized_point)

                    # if off curve, then check the curve status
                    if ( b0 == 0 ):
                        
                        if ( len(point_bay) > 2 and curve_type == 0 ):
                            
                            curve = q_bezier(point_bay[0], point_bay[1], point_bay[2])
                            #curve.display()
                            container = curve.bounding_rectangle()

                            query_quad.insert( container, curve )

                            end_of_last_curve = point_bay[2]
                            point_bay.clear()
                            point_bay.append(normalized_point)

                            
                        if ( len(point_bay) > 3 and curve_type == 1 ):

                            curve = c_bezier(point_bay[0], point_bay[1], point_bay[2], point_bay[3])
                            #curve.display()
                            container = curve.bounding_rectangle()

                            query_quad.insert( container, curve )

                            end_of_last_curve = point_bay[2]
                            point_bay.clear()
                            point_bay.append(normalized_point)

                        b1 = tag & 0b00000010
                        curve_type = b1

                last_end_point = contour_end_point+1
                
                if ( len(point_bay) == 2):  
                    
                    point = outline.points[first_end_point]
                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    curve = q_bezier(point_bay[0], point_bay[1], normalized_point)
                    #curve.display()
                    container = curve.bounding_rectangle()
                    query_quad.insert( container, curve )
                    point_bay.clear()
                    

                if ( len(point_bay) == 1):

                    point = outline.points[first_end_point]
                    # accumulate the bounding box
                    normalized_point = [ (point[0] - bbox.xMin)/(bbox.xMax-bbox.xMin), (point[1] - bbox.yMin)/(bbox.yMax-bbox.yMin) ]

                    normalized_point[1] *= (1-vertical_padding)

                    aspect_ratio = (bbox.xMax-bbox.xMin)/(bbox.yMax - bbox.yMin)*(1-vertical_padding)

                    # normalize to the aspect ratio
                    normalized_point[0] *= aspect_ratio

                    normalized_point[0] += (1-aspect_ratio)/2
                    normalized_point[1] += vertical_padding/2

                    curve = vec2(point_bay[0], normalized_point)
                    container = curve.bounding_rectangle()
                    query_quad.insert( container, curve )
                    point_bay.clear()

            last_distance = -1
            epsilon_limit = 0.1
            #iterate through the desired resolution
            for j in range(0, desired_resolution+1):
                for i in range(0, desired_resolution+1):

                    u = i/desired_resolution
                    v = j/desired_resolution
                    
                    pixel_limit = math.ceil(desired_resolution*vertical_padding/2)

                    in_margin = (j < pixel_limit) or (j > desired_resolution-pixel_limit)

                    distance = query_quad.query_closest_cell(u,v)

                    texture_coordinate = [self.cursor[0] + i, self.cursor[1] + j]

                    self.texture_data[ (texture_coordinate[1] * self.resolution[0]) + texture_coordinate[0] ] = int(((1-distance)*0.5)*255)

                    last_distance = distance

                place = "left"
                last_distance = -1
            

            if ( self.cursor[0] + desired_resolution > self.resolution[0] ):
                self.cursor[0] = 0
                self.cursor[1] += desired_resolution
            else:
                self.cursor[0] += desired_resolution
            
        #print(iteration_count[0])    

        print("done")


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

            float r = texture(tex, Texcoord).x;

            // Sample the SDF texture
            float distance = texture(tex, Texcoord).r;

            // Smooth step function for anti-aliasing
            float smoothEdge = 0.1; // Adjust this value for smoother edges

            float alpha = smoothstep(0.5 - smoothEdge, 0.5 + smoothEdge, distance);

            // Set the fragment color with the calculated alpha
            //FragColor = vec4(textColor.rgb, alpha * textColor.a);
            //frag_color = vec4(distance, distance, distance, 1.0);
            frag_color = vec4(alpha, alpha, alpha, 1.0);



            //gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n
        }\n
        '''


        program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
    
        #glSetInt(program, "tex", texture_binding_point)
        return vertex_array, element_buffer, program, atlas_texture

                
# joanRegular = TextGeometry()
# joanRegular.LoadActiveFont("fonts\\Joan-Regular.ttf")



                

        

