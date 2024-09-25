import numpy as np
import os
import sys
import math
# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from math_structures.Euler import *

from shaders.PyGLHelper import *

class BasicMesh:

    def __init__( self, geometry, material ):

        self.geometry = geometry
        self.material = material

        # store the model matrix of this mesh
        self.model_matrix = np.array([
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ], dtype=np.float32)

        # set the initial model matrix of the material
        self.material.set_model_matrix ( self.model_matrix  )

        # store internal position
        self.position = [0,0,0]
        self.euler = Euler(0,0,0)

    
    def set_position ( self, x,y,z ):

        self.model_matrix[12] = x
        self.model_matrix[13] = y
        self.model_matrix[14] = z

        self.position[0] = x
        self.position[1] = y
        self.position[2] = z

        self.material.uniforms_need_update()
    
    def get_position ( self ):
        return [self.position[0], self.position[1], self.position[2]]

    def set_euler ( self, euler ):

        ax = euler[0]*(math.pi/180)
        ay = euler[1]*(math.pi/180)
        az = euler[2]*(math.pi/180)

        cx = math.cos(ax)
        cy = math.cos(ay)
        cz = math.cos(az)

        sx = math.sin(ax)
        sy = math.sin(ay)
        sz = math.sin(az)

        # Rotation matrix for ZYX convention
        self.model_matrix[0] = cy * cz
        self.model_matrix[1] = sy*sx - cy*sz*cx
        self.model_matrix[2] = cy*sz*sx + sy*cx

        self.model_matrix[4] = sz
        self.model_matrix[5] = cz*cx
        self.model_matrix[6] = -cz*sx

        self.model_matrix[8] = -sy*cz
        self.model_matrix[9] = sy*sz*cx + cy*sx
        self.model_matrix[10] = -sy*sz*sx + cy*cx

        self.material.uniforms_need_update()


        return

    def set_axis_angle( self, axis, angle ):

        a = angle * math.pi/180

        c = math.cos(a)
        s = math.sin(a)
        t = 1-c

        ax = axis[0]
        ay = axis[1]
        az = axis[2]

        magnitude = math.sqrt ( ax*ax + ay*ay + az*az )

        if ( magnitude == 0 ):
            return
        
        ax = ax/magnitude
        ay = ay/magnitude
        az = az/magnitude

        self.model_matrix[0] = t*ax*ax + c
        self.model_matrix[1] = t*ax*ay - az*s
        self.model_matrix[2] = t*ax*az + ay*s
        
        self.model_matrix[4] = t*ax*ay + az*s
        self.model_matrix[5] = t*ay*ay + c
        self.model_matrix[6] = t*ay*az - ax*s

        self.model_matrix[8] = t*ax*az - ay*s
        self.model_matrix[9] = t*ay*az + ax*s
        self.model_matrix[10] = t*az*az + c

        self.material.uniforms_need_update()
        
    def render(self):

        self.material.program.use_program()
        self.geometry.element_buffer.bind_for_draw()

        #glUseProgram(self.material.program.program)
        #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.geometry.element_buffer.element_buffer)

        glDrawElementsInstanced(GL_TRIANGLES, self.geometry.element_buffer.elements_index, GL_UNSIGNED_INT, None, 1)



