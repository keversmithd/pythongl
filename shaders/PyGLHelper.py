import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import os


def CreateProgram(shader_sources, shader_types):
    # Compile shaders and create program
    shaders = []
    current_directory = os.getcwd()
    print(current_directory)
    for source, shader_type in zip(shader_sources, shader_types):
        source = current_directory + '\\' + source
        with open(source, 'r') as file:
            shader_source = file.read()
            shader = compileShader(shader_source, shader_type)
            shaders.append(shader)

    program = compileProgram(*shaders)

    return program


