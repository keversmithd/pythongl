import numpy as np
import os
import sys

# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *

# uniform object passed in for each element.
class layout_element_style(ctypes.Structure):

    _fields_ = [("container", ctypes.c_float * 4),
                ("parent_container", ctypes.c_float * 4),
                ("relation", ctypes.c_int * 4),
                ("color", ctypes.c_float * 4)]
    
    def __init__( self, container=(0.5,0.5,1,1), parent_container=(-1,-1,1,1), relation=(0,0,0,0), color=(1,0,0,1) ):

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

        self.color[0] = color[0]
        self.color[1] = color[1]
        self.color[2] = color[2]
        self.color[3] = color[3]

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

    def set_color(self, color):

        self.color[0] = color[0]
        self.color[1] = color[1]
        self.color[2] = color[2]
        self.color[3] = color[3]
        return

    def get_container(self):

        container = [0,0,0,0]
        #get two axis system
        a1 = np.array([self.parent_container[2] - self.parent_container[0], 0], dtype=float)
        a2 = np.array([0, self.parent_container[3] - self.parent_container[1]], dtype=float)

        if(self.relation[0] == 0):
            container[0] = self.parent_container[0] + a1[0]*self.container[0]
            container[1] = self.parent_container[1] + a2[1]*self.container[1]
            container[2] = self.parent_container[0] + a1[0]*self.container[2]
            container[3] = self.parent_container[1] + a2[1]*self.container[3]
        if(self.relation[1] == 1):
            container[0] = (self.parent_container[0]+(a1[0]/2)) + (a1[0]/2)*self.container[0]
            container[1] = (self.parent_container[1] + (a2[1]/2)) + (a2[1]/2)*self.container[1]
            container[2] = (self.parent_container[0]+(a1[0]/2)) + (a1[0]/2)*self.container[2]
            container[3] = (self.parent_container[1] + a2[1]/2) + (a2[1]/2)*self.container[3]


        return container
    
    def set_relation(self, relation):
        self.relation[0] = relation
        self.relation[1] = relation
        self.relation[2] = relation
        self.relation[3] = relation

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

        # gl objects
        self.element_mesh = simple_element_mesh()
        # vertex space
        self.element_geometry = simple_element_geometry()

        #connects to state
        self.state = state

        # links the event object up.
        self.state.event_objects.append(self)

        # if parent equals none, set style to default.

        if ( parent == None):
            self.style = layout_element_style()
        else:
            self.style = layout_element_style()
            self.link_to_parent(parent)
        
        # set program to non and create it in update_program
        self.program = None
        self.update_program()
        # creates program and links the shader material
        
        # uniform creation process [must update]
        self.make_uniform()

        # creates the uniform and sets the style information.
        self.generate_geometry()

        # stores and updates buffer data for vertex
        self.element_mesh.init_buffers(self.element_geometry.vertex_data, self.element_geometry.element_data, [(4, GL_FLOAT)], 4*4)

        # make an updated flag to determine whether this object has been updated or changed, ie its container etc.
        self.has_changed = True

    # links the parent to this object and updates the style.
    def link_to_parent(self, parent):
        
        # set the parent as permanent reference.
        self.parent = parent

        self.style.set_parent_container(parent.style.get_container())

        return

    # update to parent updates this objects style to parents new status.
    def update_to_parent(self):
        self.style.set_parent_container(self.parent.style.get_container())

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
            vec4 color;\n
        };\n

        void main()\n
        {\n
            TexCoord = vertex.zw;\n

            if ( relation.x == 0 )\n
            {\n
                vec2 b = (parent_container.zw-parent_container.xy);\n
                //vec2 t  = (container)

                vec4 l = vec4(parent_container.x + (container.x*b.x), parent_container.y + (container.y*b.y),0, 1);\n
                
                vec4 r = l + vec4((container.z*b.x), 0.0, 0.0, 0.0);\n
                vec4 rt = r + vec4(0, container.w*b.y, 0.0, 0.0);\n
                vec4 tl = l + vec4(0.0, container.w*b.y, 0.0, 0.0);\n

                vec4 ar[4] = { l,r,rt,tl };\n


                gl_Position = ar[gl_VertexID];
            }\n
            if (relation.x == 1)\n
            {\n
                vec2 b = (parent_container.zw-parent_container.xy);\n
                vec4 l = vec4( (parent_container.x + (b.x/2)) + (container.x*(b.x/2)), (parent_container.y + (b.y/2)) + (container.y*(b.y/2)),0,1 );
                vec4 r = vec4( (parent_container.x + (b.x/2)) + (container.z*(b.x/2)), (parent_container.y + (b.y/2)) + (container.y*(b.y/2)),0,1 );
                vec4 rt = vec4( (parent_container.x + (b.x/2)) + (container.z*(b.x/2)), (parent_container.y + (b.y/2)) + (container.w*(b.y/2)),0,1 );
                vec4 tl = vec4( (parent_container.x + (b.x/2)) + (container.x*(b.x/2)), (parent_container.y + (b.y/2)) + (container.w*(b.y/2)),0,1 );


                vec4 ar[4] = { l,r,rt,tl };\n

                gl_Position = ar[gl_VertexID];
            }\n

            return;
            
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
            
            
            
            
            //gl_Position = vec4( parent_space_position, 0.0, 1.0 );\n
            //gl_Position = vec4( screen_space_container.z+vertex.x, screen_space_container.w+vertex.y, 0.0, 1.0);\n
            //gl_Position = vec4(vertex.x, vertex.y, 0.0, 1.0);\n
        }\n



        '''

        fragment_shader = '''
        #version 460 core\n

        in vec2 TexCoord;\n


        //style of element
        layout (std140) uniform style {\n
            vec4 container;\n
            vec4 parent_container;\n
            ivec4 relation;\n
            vec4 color;\n
        };\n
        
        out vec4 FragColor;

        void main()\n
        {\n
            FragColor = color;\n
        }\n

        '''
        self.program = ConstProgram([vertex_shader, fragment_shader], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])

        return

    def set_style(self, container=(0.5,0.5,1.0,1.0), color=(1,0,0,1), relation=0):
        self.style.set_container(container)
        self.style.set_color(color)
        self.style.set_relation(relation)        
        self.update_uniform()
        return

    def make_uniform(self):

        self.style_uniform = glGenBuffers(1)
        glBindBuffer(GL_UNIFORM_BUFFER, self.style_uniform)
        glBufferData(GL_UNIFORM_BUFFER, ctypes.sizeof(self.style), ctypes.byref(self.style), GL_DYNAMIC_DRAW)

        self.uniform_unit = self.state.add_uniform_buffer()
        glBindBuffer(GL_UNIFORM_BUFFER, 0)
        return
    
    def update_uniform(self):
        glBindBuffer(GL_UNIFORM_BUFFER, self.style_uniform)
        #alternatively glBufferSubData
        glBufferData(GL_UNIFORM_BUFFER, ctypes.sizeof(self.style), ctypes.byref(self.style), GL_DYNAMIC_DRAW)
        glBindBuffer(GL_UNIFORM_BUFFER,0)

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

        # generate uv quad
        self.element_geometry.reset_indexes()

        self.element_geometry.resize_arrays(1, [4*4,6])

        self.element_geometry.append_vec4(0.0, 0.0, 0.0, 0.0)
        self.element_geometry.append_vec4(1.0, 0.0, 1.0, 0.0)
        self.element_geometry.append_vec4(1.0, 1.0, 1.0, 1.0)
        self.element_geometry.append_vec4(0.0, 1.0, 0.0, 1.0)

        self.element_geometry.append_element_quad(0,1,2,3)

        return

    def render(self):

        # if this objects parent has changed, then update the style uniform, as well update the event system with new coordinates using this event system id.

        if ( self.parent.has_Changed == True ):
            self.update_to_parent()
            self.update_uniform(self)

        glUseProgram(self.program)
        self.element_mesh.bind_for_draw()
        
        # set the uniform
        glSetBlock(self.program, "style", self.uniform_unit)
        glBindBufferBase(GL_UNIFORM_BUFFER, self.uniform_unit, self.style_uniform)
        
        # draw the elements
        glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None)