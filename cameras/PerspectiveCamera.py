
import numpy as np
import os
import sys

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)
from shaders.PyGLHelper import *

def perspective_projection(fov, aspect_ratio, near_plane, far_plane):
    fov_rad = np.radians(fov)
    tan_half_fov = np.tan(fov_rad / 2.0)
    
    projection_matrix = np.zeros((4, 4))
    projection_matrix[0, 0] = 1.0 / (aspect_ratio * tan_half_fov)
    projection_matrix[1, 1] = 1.0 / tan_half_fov
    projection_matrix[2, 2] = -(far_plane + near_plane) / (far_plane - near_plane)
    projection_matrix[2, 3] = -1.0
    projection_matrix[3, 2] = -(2.0 * far_plane * near_plane) / (far_plane - near_plane)
    
    return projection_matrix

# perspective camera
class PerspectiveCamera:

    def __init__(self, scene ):

        self.state = scene

        self.fov = 90
        self.projection = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ], dtype=np.float32)

        self.view = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ], dtype=np.float32)

        self.near_plane = 0.1
        self.far_plane = 100.0

        self.position = np.array([0.0, 0.0, 3.0])
        self.forward = np.array([0.0, 0.0, -1.0])
        self.up = np.array([0.0, 1.0, 0.0])

        self.previous_mouse_x = 0
        self.previous_mouse_y = 0
        self.first_mouse = True

        self.update_projection_matrix()

    def update_projection_matrix(self):
        # get current viewport width and height
        vw = self.state.vw
        vh = self.state.vh
        a = vw/vh
        
        fov_radians = np.radians(self.fov)
        tan = np.tan( fov_radians/2.0 )


        left = -1
        right = 1
        top = 1
        bottom = -1


        # self.projection[0] = 1/(a*tan)
        # self.projection[5] = 1/(tan)
        # self.projection[10] = -(self.far_plane+self.near_plane)/(self.far_plane - self.near_plane)
        # self.projection[11] = -1
        # self.projection[14] = -(2*self.far_plane*self.near_plane)/(self.far_plane - self.near_plane)


        # self.projection[0] = (2*self.near_plane)/(right-left)
        # self.projection[2] = (right+left)/(right-left)
        # self.projection[5] = (2*self.near_plane)/(top-bottom)
        # self.projection[6] = (top+bottom)/(top-bottom)
        # self.projection[10] = -(self.far_plane+self.near_plane)/(self.far_plane - self.near_plane)
        # self.projection[11] = -(2*self.far_plane*self.near_plane)/(self.far_plane - self.near_plane)
        # self.projection[14] = -1

        # near = 2
        # self.projection[0] = (near)/(right)
        # self.projection[5] = (near)/(top)
        # self.projection[10] = -1
        # self.projection[11] = -(near)
        # self.projection[14] = -1

        top = tan*self.near_plane
        right = top*a

        self.projection[0] = (self.near_plane)/right
        self.projection[5] = (self.near_plane)/top
        self.projection[10] = -(self.far_plane+self.near_plane)/(self.far_plane - self.near_plane)
        self.projection[11] = -1
        self.projection[14] = -(2*self.far_plane*self.near_plane)/(self.far_plane - self.near_plane)
        self.projection[15] = 0

        # left = -1
        # right = 1
        # top = 1
        # bottom = -1

        # self.projection[0] = (2*right)/(right-left)
        # self.projection[3] = -(right+left)/(right-left)
        # self.projection[5] = (2*top)/(top-bottom)
        # self.projection[7] = -(top+bottom)/(top-bottom)
        # self.projection[10] = -2/(self.far_plane-self.near_plane)
        # self.projection[11] = -(self.far_plane+self.near_plane)/(self.far_plane-self.near_plane)
        # self.projection[15] = 1

        #self.projection = perspective_projection(45, 800/600, 0.1, 100.0)


    def update_view_matrix(self):

        f = self.forward
        f = f/np.linalg.norm(f)

        r = np.cross( f, self.up )
        r = r/np.linalg.norm(r)
        u = np.cross(r, f)
        
        # print(f)
        # print(r)
        # print(u)

        d0  = -np.dot( r, self.position)
        d1 = -np.dot(u, self.position)
        d2 = np.dot(f, self.position)

        
        self.view[0] = r[0]
        self.view[1] = u[0]
        self.view[2] = -f[0]
        self.view[3] = 0.0

        self.view[4] = r[1]
        self.view[5] = u[1]
        self.view[6] = -f[1]
        self.view[7] = 0.0

        self.view[8] = r[2]
        self.view[9] = u[2]
        self.view[10] = -f[2]
        self.view[11] = 0.0

        self.view[12] = d0
        self.view[13] = d1
        self.view[14] = d2
        #self.view[15] = 1.0
        

        #self.view[4] = 0.0
        #self.view[8] = -2.0
        #self.view[13] = -2.0

        #self.view[4] = self.up[0]
        #self.view[5] = self.up[1]
        #self.view[6] = self.up[2]
        #self.view[14] = d1
        # self.view[1] = self.up[0]
        # self.view[5] = self.up[1]
        # self.view[9] = self.up[2]
        #self.view[14] = self.position[2]

        #self.view[8]  = f[0]
        #self.view[9]  = f[1]
        #self.view[10] = f[2]
        #self.view[15] = d2
        
    def on_mouse_move(self, x, y):

        if ( self.first_mouse == True ):
            self.previous_mouse_x = x/self.state.vw
            self.previous_mouse_y = y/self.state.vh
            self.first_mouse = False
            return
        
        dx = (x/self.state.vw)-self.previous_mouse_x
        dy = (y/self.state.vh)-self.previous_mouse_y

        nx = (x/self.state.vw)
        ny = (y/self.state.vh)

        # self.forward[0] = 0
        # self.forward[1] = 0
        # self.forward[2] = -1

        self.forward[0] += dx
        self.forward[1] -= dy

        self.previous_mouse_x = (x/self.state.vw)
        self.previous_mouse_y = (y/self.state.vh)

        self.update_view_matrix()

    def on_key_event(self, key, action):

        f = np.subtract(self.forward, self.position)
        f = f/np.linalg.norm(f)
        r = np.cross( self.up, f)
        r = r/np.linalg.norm(r)

        delta_time = self.state.delta_time
        movement_speed = 20.0

        if ( key == glfw.KEY_W ):
            self.position[2] -= movement_speed*delta_time
        if ( key == glfw.KEY_S ):
            self.position[2] += movement_speed*delta_time
        if ( key == glfw.KEY_A ):
            self.position[0] -= movement_speed*delta_time
        if ( key == glfw.KEY_D ):
            self.position[0] += movement_speed*delta_time

        
        print(self.position)

        self.update_view_matrix()

            
    
        
    
    
    
