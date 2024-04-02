import numpy as np
import os
import sys

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

class layout_element_style(ctypes.Structure):

    _fields_ = [("container", ctypes.c_float * 4),
                ("parent_container", ctypes.c_float * 4),
                ("relation", ctypes.c_int * 4),
                ("color", ctypes.c_float * 4)]
    
    def __init__( self, container=(0.5,0.5,1.0,1.0), parent_container=(-0.5,-0.5,0.5,0.5), relation=(0,0,0,0) ):
        self.container[0] = container[0]
        self.container[1] = container[1]
        self.container[2] = container[2]
        self.container[3] = container[3]  
        
        self.parent_container[0] = parent_container[0]
        self.parent_container[1] = parent_container[1]
        self.parent_container[2] = parent_container[2]
        self.parent_container[3] = parent_container[3]

        self.relation[0] = relation[0]
        self.relation[1] = relation[1]
        self.relation[2] = relation[2]
        self.relation[3] = relation[3]

    def set_container(self, container):
        self.container[0] = container[0]
        self.container[1] = container[1]
        self.container[2] = container[2]
        self.container[3] = container[3]
        return

    def set_parent_container(self, container):
        self.parent_container[0] = container[0]
        self.parent_container[1] = container[1]
        self.parent_container[2] = container[2]
        self.parent_container[3] = container[3]
        return

    def get_container(self):

        parent_space_container = np.array([self.parent_container[0],self.parent_container[1],self.parent_container[2],self.parent_container[3]], dtype=np.float32)
        local_space_container = np.array([self.container[0],self.container[1],self.container[2],self.container[3]], dtype=np.float32)

        if( self.relation[0] == 0 ):
            parent_space_container[0] = self.parent_container[0]-1
            parent_space_container[1] = self.parent_container[1]-1
            parent_space_container[2] = self.parent_container[2]
            parent_space_container[3] = self.parent_container[3]
            
        if( self.relation[0] == 1 ):
            parent_space_container[0] = self.parent_container[0]
            parent_space_container[1] = self.parent_container[1]
            parent_space_container[2] = self.parent_container[2]
            parent_space_container[3] = self.parent_container[3]

        Px = np.array([parent_space_container[2], parent_space_container[1]]) - np.array([parent_space_container[0], parent_space_container[1]])
        Py = np.array([parent_space_container[0], parent_space_container[3]]) - np.array([parent_space_container[0], parent_space_container[1]])
        Pxl = np.linalg.norm(Px)
        Pyl = np.linalg.norm(Py)

        Lx = np.array([local_space_container[2], local_space_container[1]]) - np.array([local_space_container[0], local_space_container[1]])
        Ly = np.array([local_space_container[0], local_space_container[3]]) - np.array([local_space_container[0], local_space_container[1]])
        Lxl = np.linalg.norm(Lx)
        Lyl = np.linalg.norm(Ly)

        if( local_space_container[2] < 0 ):
            Lxl = Lxl * -1
        
        if( local_space_container[3] < 0 ):
            Lyl = Lyl * -1

        

        return [parent_space_container[0] + local_space_container[0]*Pxl, parent_space_container[1] + local_space_container[1]*Pyl,
        parent_space_container[0] + local_space_container[2]*Pxl, parent_space_container[1] + local_space_container[3]*Pyl]
        

    def translate_container(self, translation):
        self.container[0] = self.container[0] + translation[0]
        self.container[1] = self.container[1] + translation[1]
        self.container[2] = self.container[2] + translation[0]
        self.container[3] = self.container[3] + translation[1]
        return
        
        


    def set_parent_container(self, container):
        self.parent_container[0] = container[0]
        self.parent_container[1] = container[1]
        self.parent_container[2] = container[2]
        self.parent_container[3] = container[3] 
        return
     
class layout_element:
    def __init__(self, state, parent=None):

        self.element_mesh = simple_element_mesh()
        self.element_geometry = simple_element_geometry()

        self.state = state
        self.program = None

        self.state.event_objects.append(self)

        self.parent = parent

        self.style = layout_element_style()

        self.previous_local_mouse = None
        self.was_dragged = False

        self.update_program()
        self.make_uniform()
        self.generate_geometry()
        self.element_mesh.init_buffers(self.element_geometry.vertex_data, self.element_geometry.element_data, [(4, GL_FLOAT)], 4*4)

    def link_to_parent(self, parent, container):
        self.parent = parent

        self.style.set_parent_container(parent.style.get_container())
        self.style.set_container(container)


        return

    def update_program(self):

        vertex_shader = '''
        #version 460 core\n
        layout(location = 0) in vec4 vertex;\n
        out vec2 TexCoord;\n

        //style of element
        layout (std140) uniform style {\n
            vec4 container;\n
            vec4 parent_container;\n
            ivec4 relation;\n
        };\n

        void main()\n
        {\n
            TexCoord = vertex.zw;\n

            
            vec4 screen_space_container = vec4( container.x, container.y, container.z, container.w );\n
            vec4 parent_space_container = vec4( parent_container.x-1, parent_container.y-1, parent_container.z, parent_container.w );\n
            if( relation.x == 0 )\n
            {\n
                parent_space_container = vec4( parent_container.x-1, parent_container.y-1, parent_container.z, parent_container.w  );\n
            }\n
            if( relation.x == 1 )\n
            {\n
                parent_space_container = vec4( parent_container.x, parent_container.y, parent_container.z, parent_container.w  );\n
            }\n
            
            // to know which vertex we represent with our box
            int vertex_id = gl_VertexID;\n
            
            // Unpacking parent space container
            vec2 Px = vec2(parent_space_container.z, parent_space_container.y) - vec2(parent_space_container.x, parent_space_container.y);\n
            vec2 Py = vec2(parent_space_container.x, parent_space_container.w) - vec2(parent_space_container.x, parent_space_container.y);\n
            float Pxl = length(Px);\n
            float Pyl = length(Py);\n

            // Unpacking local space container
            vec2 Lx = vec2(screen_space_container.z, screen_space_container.y) - vec2(screen_space_container.x, screen_space_container.y);\n
            vec2 Ly = vec2(screen_space_container.x, screen_space_container.w) - vec2(screen_space_container.x, screen_space_container.y);\n
            //float Lxl = length(Lx) * (-1 * int(screen_space_container.z < 0));\n
            //float Lyl = length(Ly) * (-1 * int(screen_space_container.w < 0));\n

            float Lxl = length(Lx);\n
            float Lyl = length(Ly);\n

            if(screen_space_container.z < 0)\n
            {\n
                Lxl = Lxl * -1;\n
            }\n
            
            if(screen_space_container.w < 0)\n
            {\n
                Lyl = Lyl * -1;\n
            }\n

            vec2 local_space_position = container.xy + vec2( vertex.x * Lxl, vertex.y * Lyl);\n
            vec2 parent_space_position = parent_space_container.xy + vec2( local_space_position.x * Pxl, local_space_position.y * Pyl);\n
            
            
            
            
            gl_Position = vec4( parent_space_position, 0.0, 1.0 );\n
            //gl_Position = vec4( screen_space_container.z+vertex.x, screen_space_container.w+vertex.y, 0.0, 1.0);\n
            //gl_Position = vec4(vertex.x, vertex.y, 0.0, 1.0);\n
        }\n



        '''

        fragment_shader = '''
        #version 460 core\n

        in vec2 TexCoord;\n
        
        void main()\n
        {\n
            gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);\n
        }\n

        '''
        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])

        return

    def make_uniform(self):
        self.style_uniform = glGenBuffers(1)
        glBindBuffer(GL_UNIFORM_BUFFER, self.style_uniform)
        glBufferData(GL_UNIFORM_BUFFER, ctypes.sizeof(self.style), ctypes.byref(self.style), GL_DYNAMIC_DRAW)
        self.uniform_unit = self.state.add_uniform_buffer()
        glBindBuffer(GL_UNIFORM_BUFFER, 0)
        return

    def on_mouse_move(self, x, y):
        x = x/self.state.vw
        y = (self.state.vh-y)/self.state.vh
        x = (x*2) - 1
        y = (y*2) - 1

        transformed_container = self.style.get_container()

        if(x > transformed_container[0] and x < transformed_container[2] and y > transformed_container[1] and y < transformed_container[3]):

            if(glfw.get_mouse_button(self.state.window, glfw.MOUSE_BUTTON_LEFT) == glfw.PRESS):
                
                if(self.previous_local_mouse != None):
                    dx = x - self.previous_local_mouse[0]
                    dy = y - self.previous_local_mouse[1]
                    self.style.translate_container([dx,dy])
                    glBindBuffer(GL_UNIFORM_BUFFER, self.style_uniform)
                    glBufferSubData(GL_UNIFORM_BUFFER, 0, 4*4, ctypes.byref(self.style))
                    glBindBuffer(GL_UNIFORM_BUFFER, 0)
                    self.previous_local_mouse = [x,y]
                    self.was_dragged = True
                    return
                else: self.previous_local_mouse = [x,y]

    def on_left_click(self):

        x = self.state.mx/self.state.vw
        y = (self.state.vh-self.state.my)/self.state.vh
        x = (2*x)-1
        y = (2*y)-1

        transformed_container = self.style.get_container()

        if( x > transformed_container[0] and x < transformed_container[2] and y > transformed_container[1] and y < transformed_container[3] ):
            print("clicked")
        

        return

    def generate_geometry(self):

        self.element_geometry.reset_indexes()

        self.element_geometry.resize_arrays(1, [4*4,6])

        self.element_geometry.append_vec4(0.0, 0.0, 0.0, 0.0)
        self.element_geometry.append_vec4(1.0, 0.0, 1.0, 0.0)
        self.element_geometry.append_vec4(1.0, 1.0, 1.0, 1.0)
        self.element_geometry.append_vec4(0.0, 1.0, 0.0, 1.0)

        self.element_geometry.append_element_quad(0,1,2,3)

        return

    def draw(self):

        glUseProgram(self.program)
        self.element_mesh.bind_for_draw()
        
        glSetBlock(self.program, "style", self.uniform_unit)
        glBindBufferBase(GL_UNIFORM_BUFFER, self.uniform_unit, self.style_uniform)
        
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)