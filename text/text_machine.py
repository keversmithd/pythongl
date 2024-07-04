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

from shaders.DataTexture import *

# text object to be used like a troika text.
class text:
    def __init__(self, text = ""):

        self.text = text
        
        # location of the text.
        self.location = [0.0, 0.0]
        self.fontSize = 1.0

        # the container of parent for overflow purposes
        self.parent_container = [0.0, 0.0, 1.0, 1.0]
        # the container after processing of the current screen space text
        self.container = [0.0, 0.0, 0.0, 0.0]
        # choose the color of the text here.
        self.color = [0.0, 0.0, 0.0, 0.0]


        # reference to the text_managerowner
        # for updating on the fly with the indexes into the individual characters
        # format bounding container, parent container, uvs, color -- in sequence per character
        self.group_id = []

        self.text_manager = None

        # store unit to tell whether the text has been added to the group update in the text manager
        self.in_update = False
    
    # a host of setters for when one wishes to change something
    def set_position(self, new_position):

        self.location = new_position
        
        if ( self.text_manager != None and self.in_update == False):
            self.text_manager.group_updates.append(self)
            self.in_update = True

    def set_text(self, new_text):
        self.text = new_text

        if ( self.text_manager != None and self.in_update == False ):
            self.text_manager.group_updates.append(self)
            self.in_update = True

    

# text machine is provided either an atlas name, or possibly a text geometry name base
class text_machine:


    def __init__(self, state, atlas_name):

        if ( atlas_name not in state.texture_atlases ):
            print ( "unknown atlas ")
            self.atlas = None
            return
        
        self.atlas = state.texture_atlases[atlas_name]

        # Use a texture uniform for styles within the character placement and color.
        # Format
        # {
        #  vec4 container
        #  vec4 parent_container
        #  vec4 color
        # }
        self.text_data = DataTexture(state, 100, 0, None, {
            "dimension": "1D",
            "internal_format" : GL_RGBA32F,
            "format" : GL_RGBA,
            "type" : GL_FLOAT
        }) 
        # Label the format size in terms of pixels per layout
        self.text_data_format = 4

        # Generate the program
        self.program = None
        self.make_program()

        # Generate the mesh
        self.element_buffer = InterleavedElementBuffer({
            "position" : 3
        })
        self.make_mesh()

        # Character count for the amount of text characters draw
        self.char_count = 0
        
        # Store the group ids that need to be updated
        self.group_updates = []
    
        return

    def make_program(self):

        vertex_shader = '''
        #version 460 core
        layout ( location = 0 ) in vec3 position;
        
        // Uniform with styles of format
        // { [vec4 container, vec4 parent_container, vec4 color] }
        uniform sampler1D styles;

        // Size of a single style in the styles sampler
        uniform int style_size;

        // Transforms from the bottom left origin of the parent container.
        vec3 transform_position( vec4 parent_container, vec4 container )
        {
            
            vec3 transformation;
            vec3 p_x = vec3(parent_container.z-parent_container.x, 0.0, 0.0 );
            vec3 p_y = vec3(0.0, parent_container.w-parent_container.y, 0.0 );
            vec3 o = vec3(parent_container.x, parent_container.y, 0.0);

            if ( gl_VertexID % 4 == 0 )
            {
                transformation = o + (p_x*container.x) + (p_y*container.y);
            }

            if ( gl_VertexID % 4 == 1 )
            {
                transformation = o + (p_x*container.z) + (p_y*container.y);
            }

            if ( gl_VertexID % 4 == 2 )
            {
                transformation = o + (p_x*container.z) + (p_y*container.w);
            }

            if ( gl_VertexID % 4 == 3 )
            {
                transformation = o + (p_x*container.x) + (p_y*container.w);
            }

            return transformation;
            
        }

        // Get the current uv based on vertex ID and the vec4 of uvs provided in the styles sampler1D.
        vec2 get_uv( vec4 uv_map )
        {
            
            vec2 uv = vec2(1.0);

            if ( gl_VertexID % 4 == 0 )
            {
                uv.x = uv_map.x;
                uv.y = uv_map.y;
            }

            if ( gl_VertexID % 4 == 1 )
            {
                uv.x = uv_map.z;
                uv.y = uv_map.y;
            }

            if ( gl_VertexID % 4 == 2 )
            {
                uv.x = uv_map.z;
                uv.y = uv_map.w;
            }

            if ( gl_VertexID % 4 == 3 )
            {
                uv.x = uv_map.x;
                uv.y = uv_map.w;
            }

            return uv;
        }

        out vertex_data
        {
            vec4 color;
            vec2 uv;
            float id;

        } out_data;

        void main()
        {
            // Get the 
            int uv = gl_InstanceID*style_size;
            
            // According to the format the the style itself.
            vec4 container = texelFetch(styles, uv, 0);
            vec4 parent_container = texelFetch(styles, uv+1, 0);
            vec4 color = texelFetch(styles, uv+2, 0);
            vec4 uvs = texelFetch(styles, uv+3, 0);

            vec3 transformation = transform_position( parent_container, container );

            // Output data
            out_data.color = color;
           
            out_data.uv = get_uv(uvs);


            gl_Position = vec4(transformation, 1.0);
        }

        '''

        fragment_shader = '''
        #version 460 core
    
        // Add the uniform sampler2D Atlas in here
        uniform sampler2D atlas;

        in vertex_data
        {
            vec4 color;
            vec2 uv;
            float id;

        } in_data;

        out vec4 color;

        void main()
        {

            float text_distance = texture(atlas, in_data.uv).x;
            color = vec4( text_distance, text_distance, 1.0, 1.0);
        }

        '''

        self.program = ShaderProgram({
            "vertex_shader": vertex_shader,
            "fragment_shader": fragment_shader,
            "uniforms" : {
                "styles" : { "type": "DataTexture", "value": self.text_data },
                "style_size" : { "type": "int", "value" : [ self.text_data_format ] },
                "atlas" : {"type": "texture2D", "value" : [ self.atlas.atlas_texture, self.atlas.texture_unit ]}
            }
        })

    def make_mesh(self):

        self.element_buffer.allocate(4)

        self.element_buffer.push("position", [-1,-1,0])
        self.element_buffer.push("position", [1,-1,0])
        self.element_buffer.push("position", [1,1,0])
        self.element_buffer.push("position", [-1,1,0])

        self.element_buffer.push_index([0,1,2,0,2,3], 6)
        self.element_buffer.sync_buffers()

    # adds text to the text machine
    def add(self, text_object):
        
        text_object.text_manager = self

        cursor = [text_object.location[0], text_object.location[1]]

        # iterate through the text object text.
        for c in range(0, len(text_object.text)):

            # get the character from the text object
            character = text_object.text[c]
            character_ord = ord(character)

            #access the atlas
            if ( character_ord in self.atlas.charmap ):
                char_detail = self.atlas.charmap[character_ord]
                lower_u = char_detail[0]
                lower_v = char_detail[1]
                upper_u = char_detail[2]
                upper_v = char_detail[3]
                width = char_detail[4]
                height = char_detail[5]
                horz_advance = char_detail[6]
                vert_advance = char_detail[7]

                cursor[0] += horz_advance
                # build the bounding container
                bounding_container = [ cursor[0], cursor[1]+vert_advance, cursor[0]+width, cursor[1]+height+vert_advance ]
                
                # the head of the character chunk will be stored and added to the text object.
                id0 = self.text_data.push_vector( bounding_container )
                id1 = self.text_data.push_vector( [0.0, 0.0, 1.0, 1.0] )
                id2 = self.text_data.push_vector( [1.0, 1.0, 1.0, 1.0] )
                id3 = self.text_data.push_vector( [lower_u, lower_v, upper_u, upper_v ])

                text_object.group_id.append(id0)
                text_object.group_id.append(id1)
                text_object.group_id.append(id2)
                text_object.group_id.append(id3)

                self.char_count += 1

                cursor[0] += width

        return     

    # group id semantics
    def update_group_id(self, text_object):

        cursor = [text_object.location[0], text_object.location[1]]
        group_id = text_object.group_id

        # called from within the text object itself.
        for i in range(0,len(text_object.text)):
            
            # get the character from the text object
            character = text_object.text[i]
            character_ord = ord(character)

            #access the atlas
            if ( character_ord in self.atlas.charmap ):
                char_detail = self.atlas.charmap[character_ord]
                lower_u = char_detail[0]
                lower_v = char_detail[1]
                upper_u = char_detail[2]
                upper_v = char_detail[3]
                width = char_detail[4]
                height = char_detail[5]
                horz_advance = char_detail[6]
                vert_advance = char_detail[7]
                
                cursor[0] += horz_advance
                # build the bounding container
                bounding_container = [ cursor[0], cursor[1]+vert_advance, cursor[0]+width, cursor[1]+height+vert_advance ]

                

                self.text_data.update_vector( bounding_container, group_id[(i*4)] )
                self.text_data.update_vector( [0.0, 0.0, 1.0, 1.0], group_id[(i*4)+1] )
                self.text_data.update_vector(  [1.0, 1.0, 1.0, 1.0], group_id[(i*4)+2] )
                self.text_data.update_vector( [lower_u, lower_v, upper_u, upper_v ], group_id[(i*4)+3] )

                cursor[0] += width

        self.program.uniforms_need_update = True
        text_object.in_update = False

    # updates all group ids in the id bay
    def update_group_ids(self):
        
        for i in range(0, len(self.group_updates)):

            self.update_group_id(self.group_updates[i])
        
        self.group_updates.clear()

    def render(self):

        if ( self.char_count == 0 ):
            return

        self.program.use_program()
        self.element_buffer.bind_for_draw()
        self.update_group_ids()

        glDrawElementsInstanced(GL_TRIANGLES, 6, GL_UNSIGNED_INT, None, self.char_count)
    