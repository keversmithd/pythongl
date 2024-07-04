
import numpy as np
import os
import sys

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)
from shaders.PyGLHelper import *

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
        self.far_plane = 1000.0

        self.position = np.array([0.0, 0.0, 0.0])
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
        f = 1.0 / np.tan( fov_radians/2.0 )

        self.projection[0] = f / a
        self.projection[5] = f
        self.projection[10] = (self.far_plane+self.near_plane)/(self.near_plane-self.far_plane)
        self.projection[11] = (2*self.far_plane*self.near_plane)/(self.near_plane-self.far_plane)
        self.projection[14] = -1.0

    def update_view_matrix(self):

        f = self.forward/np.linalg.norm(self.forward)
        r = np.cross(f, self.up)
        u = np.cross(r,f)
        
        #print(r)

        d0  = -np.dot(r, self.position)
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

        self.view[12] = -np.dot(r, self.position)
        self.view[13] = -np.dot(u, self.position)
        self.view[14] = np.dot(f, self.position)
        self.view[15] = 1.0
        

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

        print(dx,dy)

        self.forward[0] += dx*3.0
        self.forward[1] += dy*3.0

        self.previous_mouse_x = (x/self.state.vw)
        self.previous_mouse_y = (y/self.state.vh)

        self.update_view_matrix()

    def on_key_event(self, key, action):

        f = self.forward/np.linalg.norm(self.forward)
        delta_time = self.state.delta_time
        movement_speed = 3.0
        if ( key == glfw.KEY_W ):
            self.position[0] -= f[0]*movement_speed*delta_time
            self.position[1] += f[1]*movement_speed*delta_time
            self.position[2] += f[2]*movement_speed*delta_time
        if ( key == glfw.KEY_S ):
            self.position[0] -= f[0]*movement_speed*delta_time
            self.position[1] -= f[1]*movement_speed*delta_time
            self.position[2] -= f[2]*movement_speed*delta_time
        if ( key == glfw.KEY_A ):
            self.position[0] -= movement_speed*delta_time
        if ( key == glfw.KEY_D ):
            self.position[0] += movement_speed*delta_time
        
        self.update_view_matrix()

            
    
        
    
    
    
