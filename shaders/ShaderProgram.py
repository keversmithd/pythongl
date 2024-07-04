import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

# Shader program helps keep track of uniforms and all things program!

class ShaderProgram():

    def __init__(self, program_options):      

        self.program_options = program_options

        if ( "uniforms" in program_options ):
            self.uniforms = program_options["uniforms"]
        else:
            self.uniforms = None

        self.create_program(program_options)

        self.uniforms_need_update = True

        # Use callback for uniform type handlers
        self.uniform_type_handlers = {
            "int" : self.uniform_int,
            "uniform buffer" : self.uniform_buffer,
            "texture1D" : self.uniform_texture1D,
            "texture2D" : self.uniform_texture2D,
            "DataTexture" : self.uniform_data_texture
        }

        self.active_camera = None

        if ( "camera" in program_options ):
            self.active_camera = program_options["camera"]
          
        return

    # Uniform data texture has the value pegged at a DataTexture object so that it can be updated if needed as well as encompasses all dimensional types
    def uniform_data_texture(self, uniform_name, value):
        location = glGetUniformLocation(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
        
        # call update on the data texture so that it can update its contents.
        value.update()

        glActiveTexture(GL_TEXTURE0 + value.texture_unit)
        glBindTexture( value.texture_bind, value.texture_obj)
        glUniform1i( location, value.texture_unit )


    # Uniform type handlers
    def uniform_int(self, uniform_name, value):
        location = glGetUniformLocation(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
        glUniform1i( location, value[0] )
        
        return

    def uniform_buffer(self, uniform_name, value):
        
        location = glGetUniformBlockIndex(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
            
        glUniformBlockBinding(self.program, location, value[1])
        glBindBufferBase(GL_UNIFORM_BUFFER, value[1], value[0])

        return

    def uniform_texture1D(self, uniform_name, value):

        location = glGetUniformLocation(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
            
        glActiveTexture(GL_TEXTURE0 + value[1])
        glBindTexture(GL_TEXTURE_1D, value[0])

        glUniform1i( location, value[1] )

        return

    def uniform_texture2D(self, uniform_name, value):

        location = glGetUniformLocation(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
            
        glActiveTexture(GL_TEXTURE0 + value[1])
        glBindTexture(GL_TEXTURE_2D, value[0])

        glUniform1i( location, value[1] )

        return

    # numpy flat array 
    def uniform_mat4(self, uniform_name, value):
        location = glGetUniformLocation(self.program, uniform_name)
        if(location == -1 or location == 4294967295):
            print("Uniform location not found!")
            return
        
        glUniformMatrix4fv(location, 1, GL_FALSE, value)



    def create_program(self,program_options):

        if program_options["vertex_shader"] == None or program_options["fragment_shader"] == None:
            print("Shader Program invalid programs")
            return

        possible_shaders = ["vertex_shader", "fragment_shader", "geometry_shader"]
        shader_types = {"vertex_shader": GL_VERTEX_SHADER, "fragment_shader": GL_FRAGMENT_SHADER, "geometry_shader": GL_GEOMETRY_SHADER }

        # get the current directory.
        current_directory = os.getcwd()

        # set up shader array
        shader_list = []

        # for possible shaders
        for shader in possible_shaders:
            # shader exists in the program options
            if shader in program_options:
                # get the shader type
                shader_type = shader_types[shader]
                
                if ( len(program_options) < 22 ):
                    potential_source = ""
                else:
                    # if the shader exists check whether its a valid path location
                    potential_source = current_directory + '\\' + program_options[shader]


                if os.path.isfile(potential_source):
                    # if it is open as read
                    with open(source, 'r') as file:
                        shader_source = file.read()
                        # read the full file
                        shader_attachment = compileShader(shader_source, shader_type)
                        shader_list.append(shader_attachment)
                else:
                    shader_source = program_options[shader]
                    shader_attachment = compileShader(shader_source, shader_type)
                    shader_list.append(shader_attachment)


        self.program = compileProgram(*shader_list)

    def set_uniform(uniform_name, uniform_type, value):
        self.uniforms[uniform_name].type = uniform_type
        self.uniforms[uniform_name].value = value
        self.uniforms_need_update = True

    # call when wanting to retrieve the latest activate camera projection and view etcs, and upload it to the program!
    # implement in the future custom projection names and custom matrices on the camera itself throguh the actual camera object
    def update_camera(self):

        if ( self.active_camera != None ):
            self.uniform_mat4( "projection", self.active_camera[0].projection )
            self.uniform_mat4( "view", self.active_camera[0].view )
            

    def use_program(self):
        # use the program
        glUseProgram(self.program)

        self.update_camera()

        if self.uniforms != None and self.uniforms_need_update == True:
            for uniform_name,uniform_key in self.uniforms.items():
                self.uniform_type_handlers[uniform_key["type"]]( uniform_name, uniform_key["value"] )

            self.uniforms_need_update = False




