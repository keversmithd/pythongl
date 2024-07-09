import numpy as np
import os
import sys

# append workspace directory to the system path for file usage.
workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *
from shaders.ElementBuffer import InterleavedElementBuffer
from shaders.ShaderProgram import ShaderProgram
from shaders.UniformBuffer import UniformBuffer

# Generate Element Unit
class layout_style:
    def __init__(self):
        self.container=(0.0,0.0,1,1)
        self.parent_container=(-1,-1,1,1)
        self.relation=(1,0,0,0)
        self.color=(1,0,0,1)
        return

# Base Class : A Psuedo Data Class
class layout_style_dataclass:
    
    def __init__(self, size):

        # Format
        # Container Vec4 : Color Vec4 :

        # Set up the data class size as the number of floats in a dataclass unit.
        self.dataclass_size = 16

        # Store data for the dataclass uniform
        self.data = np.zeros(self.dataclass_size*size, dtype=np.float32)
        # Store the currently allocated number of dataclasses
        self.data_allocated = self.dataclass_size*size

        # Current size
        self.capacity = size

        # Current push back unit for inner array.
        self.tail = 0

        # Array of useable indexes if neccecary.
        self.reusable_ids = []

        # Array of offset indexes for different style portions
        self.attribute_offsets = {
            "container" : 0,
            "parent_container" : 4,
            "relation": 8,
            "color": 12,
        }

        return
    
    # Resize the data if neccecary
    def resize(self):
        
        self.data = np.resize(  self.data, max(1,self.data_allocated*2))
        self.capacity = self.capacity*2
        self.data_allocated = max(1,self.data_allocated*2)

    def set_container(self, id, value):

        offset_index = self.attribute_offsets["container"]

        self.data[offset_index + (self.tail*self.dataclass_size)] = value[0]
        self.data[offset_index + (self.tail*self.dataclass_size)+1] = value[1]
        self.data[offset_index + (self.tail*self.dataclass_size)+2] = value[2]
        self.data[offset_index + (self.tail*self.dataclass_size)+3] = value[3]
    
    def set_color(self, id, value):

        offset_index = self.attribute_offsets["color"]

        self.data[offset_index + (self.tail*self.dataclass_size)] = value[0]
        self.data[offset_index + (self.tail*self.dataclass_size)+1] = value[1]
        self.data[offset_index + (self.tail*self.dataclass_size)+2] = value[2]
        self.data[offset_index + (self.tail*self.dataclass_size)+3] = value[3]
    
    def set_parent_container(self, id, value):

        offset_index = self.attribute_offsets["parent_container"]

        self.data[offset_index + (self.tail*self.dataclass_size)] = value[0]
        self.data[offset_index + (self.tail*self.dataclass_size)+1] = value[1]
        self.data[offset_index + (self.tail*self.dataclass_size)+2] = value[2]
        self.data[offset_index + (self.tail*self.dataclass_size)+3] = value[3]
    
    def set_relation(self, id, value):

        offset_index = self.attribute_offsets["relation"]

        self.data[offset_index + (self.tail*self.dataclass_size)] = value[0]
        self.data[offset_index + (self.tail*self.dataclass_size)+1] = value[1]
        self.data[offset_index + (self.tail*self.dataclass_size)+2] = value[2]
        self.data[offset_index + (self.tail*self.dataclass_size)+3] = value[3]

    def push(self, style):

        if ( self.tail >= self.capacity ):
            self.resize()

        element_id = self.tail

        self.set_container(element_id, style.container)
        self.set_parent_container(element_id, style.parent_container)
        self.set_color(element_id, style.color)
        self.set_relation(element_id, style.relation)

        self.tail += 1

        return
        
# Uses instanced draw call with the uniforms neccecary
class layout_element_machine:

    def __init__(self, state):

        # Set state of the machine
        self.state = state
        
        # Unfirom buffer dataclass
        self.style_dataclass = layout_style_dataclass(1)

        # Create the uniform buffer
        self.style_uniform_buffer = UniformBuffer(state)

        #Element mesh for use in rendering the instanced elements
        self.element_buffer = InterleavedElementBuffer()

        # Create the mesh
        self.make_mesh()
        
        # Create the program object
        self.make_program()

        # Keep track of instances being transmitted
        self.element_count = 0

        # Keep track of the uniform buffer needs to be updated
        self.uniform_buffer_needsUpdate = False
 
    def make_mesh(self):

        self.element_buffer.allocate(4)
        self.element_buffer.push("position", [-1,-1,0])
        self.element_buffer.push("normal", [0,0,1])
        self.element_buffer.push("uv", [0,0])

        self.element_buffer.push("position", [1,-1,0])
        self.element_buffer.push("normal", [0,0,1])
        self.element_buffer.push("uv", [1,0])

        self.element_buffer.push("position", [1,1,0])
        self.element_buffer.push("normal", [0,0,1])
        self.element_buffer.push("uv", [1,1])

        self.element_buffer.push("position", [-1,1,0])
        self.element_buffer.push("normal", [0,0,1])
        self.element_buffer.push("uv", [0,1])

        self.element_buffer.push_index([0,1,2,0,2,3], 6)
        
        self.element_buffer.sync_buffers()

    def make_program(self):

        vertex_shader = '''
        #version 460 core
        layout(location = 0) in vec3 position;
        layout(location = 1) in vec3 normal;
        layout(location = 2) in vec2 uv;

        struct element_style {
            vec4 container;
            vec4 parent_container;
            vec4 relation;
            vec4 color;
        };

        layout (std140) uniform style_block {
            element_style styles[1];
        };

        vec3 relative_to_center(vec4 container, vec4 parent_container)
        {

            // Set up parent container axes on x and y, unormalized of course.
            vec3 p_x = vec3((parent_container.z-parent_container.x)/2, 0, 0  );
            vec3 p_y = vec3(0, (parent_container.w-parent_container.y)/2, 0 );
            // Set up parent container origin
            vec3 p_o = vec3(parent_container.x, parent_container.y, 0) + p_x + p_y;

            if ( gl_VertexID % 4 == 0 )
            {
                
                return p_o + (p_x*container.x) + (p_y*container.y);
            
            }
            if ( gl_VertexID % 4 == 1 )
            {
                return p_o + (p_x*container.z) + (p_y*container.y);
            }
            if ( gl_VertexID % 4 == 2 )
            {
                return p_o + (p_x*container.z) + (p_y*container.w);
            }
            if ( gl_VertexID % 4 == 3 )
            {
                return p_o + (p_x*container.x) + (p_y*container.w);
            }

        }

        vec3 relative_to_origin(vec4 container, vec4 parent_container)
        {
            vec3 p_x = vec3( parent_container.z-parent_container.x, 0, 0  );
            vec3 p_y = vec3( 0, parent_container.w-parent_container.y, 0 );
            vec3 p_o = vec3( parent_container.x, parent_container.y, 0 );

            if ( gl_VertexID % 4 == 0 )
            {
                return p_o + (p_x*container.x) + (p_y*container.y);
            }
            if ( gl_VertexID % 4 == 1 )
            {
                return p_o + (p_x*container.z) + (p_y*container.y);
            }
            if ( gl_VertexID % 4 == 2 )
            {
                return p_o + (p_x*container.z) + (p_y*container.w);
            }
            if ( gl_VertexID % 4 == 3 )
            {
                return p_o + (p_x*container.x) + (p_y*container.w);
            }

        }

        out vertex_data {
            vec4 color;
        } out_data;

        void main()
        {
            // Unpack the element
            vec4 element_container = styles[gl_InstanceID].container;
            vec4 element_parent_container = styles[gl_InstanceID].parent_container;
            vec4 relation = styles[gl_InstanceID].relation;
            vec4 color = styles[gl_InstanceID].color;
            

            // Set up position or pos unit
            vec3 pos;

            if ( relation.x == 0 )
            {
                pos = relative_to_center(element_container, element_parent_container);
            }
            if ( relation.x == 1 )
            {
                pos = relative_to_origin(element_container, element_parent_container);
            }

        
            // Submit outdata for the color of the layout element.
            out_data.color = color;

            gl_Position = vec4(pos, 1.0);
        }

        '''

        fragment_shader = '''
        #version 460 core

        in vertex_data {

            vec4 color;
        } in_data;


        out vec4 color;
        void main()
        {
            color = in_data.color;
        }
        '''

        self.program = ShaderProgram({
            "vertex_shader": vertex_shader,
            "fragment_shader": fragment_shader,
            "uniforms" : {
                "style_block": { "type": "uniform buffer", "value": [self.style_uniform_buffer.uniform_buffer, self.style_uniform_buffer.uniform_index] }
            }
        })


        return

    def push_element(self, style):

        self.style_dataclass.push(style)
        self.element_count += 1
        self.uniform_buffer_needsUpdate = True

    def render(self):

        if ( self.uniform_buffer_needsUpdate == True ):
            self.style_uniform_buffer.set_buffer(self.style_dataclass.data)
            self.uniform_buffer_needsUpdate = False

        self.program.use_program()

        glBindVertexArray(self.element_buffer.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer.element_buffer)
        glDrawElementsInstanced(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None, self.element_count)


    

        