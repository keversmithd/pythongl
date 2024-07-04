import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import os
import ctypes
import numpy as np

#window
def glDebugOutput(source, type, id, severity, length, message, userParam):
    # Ignore non-significant error/warning codes
    if id == 131169 or id == 131185 or id == 131218 or id == 131204:
        return

    print("---------------")
    print(f"Debug message ({id}): {message}")
    
    if source == GL_DEBUG_SOURCE_API:
        print("Source: API")
    elif source == GL_DEBUG_SOURCE_WINDOW_SYSTEM:
        print("Source: Window System")
    elif source == GL_DEBUG_SOURCE_SHADER_COMPILER:
        print("Source: Shader Compiler")
    elif source == GL_DEBUG_SOURCE_THIRD_PARTY:
        print("Source: Third Party")
    elif source == GL_DEBUG_SOURCE_APPLICATION:
        print("Source: Application")
    elif source == GL_DEBUG_SOURCE_OTHER:
        print("Source: Other")

    if type == GL_DEBUG_TYPE_ERROR:
        print("Type: Error")
    elif type == GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR:
        print("Type: Deprecated Behavior")
    elif type == GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR:
        print("Type: Undefined Behavior")
    elif type == GL_DEBUG_TYPE_PORTABILITY:
        print("Type: Portability")
    elif type == GL_DEBUG_TYPE_PERFORMANCE:
        print("Type: Performance")
    elif type == GL_DEBUG_TYPE_MARKER:
        print("Type: Marker")
    elif type == GL_DEBUG_TYPE_PUSH_GROUP:
        print("Type: Push Group")
    elif type == GL_DEBUG_TYPE_POP_GROUP:
        print("Type: Pop Group")
    elif type == GL_DEBUG_TYPE_OTHER:
        print("Type: Other")

    if severity == GL_DEBUG_SEVERITY_HIGH:
        print("Severity: High")
    elif severity == GL_DEBUG_SEVERITY_MEDIUM:
        print("Severity: Medium")
    elif severity == GL_DEBUG_SEVERITY_LOW:
        print("Severity: Low")
    elif severity == GL_DEBUG_SEVERITY_NOTIFICATION:
        print("Severity: Notification")

    print()

    raise Exception("Bad")

def initWindow(height, width, DebugOutput, name, window_setup, state):
    if not glfw.init():
        return

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    if(DebugOutput == True):
        glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, GL_TRUE)
    # Create a window
    window = glfw.create_window(height, width, name, None, None)
    if not window:
        glfw.terminate()
        return
    
    # Make the window's OpenGL context current
    glfw.make_context_current(window)
    glfw.swap_interval(1)

    

    if(DebugOutput == True):
        flags = 0
        glGetIntegerv(GL_CONTEXT_FLAGS, flags)
        if( flags & GL_CONTEXT_FLAG_DEBUG_BIT):
            glEnable(GL_DEBUG_OUTPUT)
            glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
            glDebugMessageCallback(glDebugOutput, None)
            glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, None, GL_TRUE)

    window_setup(window, state)
    
    return window

def CreateProgram(shader_sources, shader_types):
    # Compile shaders and create program
    shaders = []
    current_directory = os.getcwd()
    # print(current_directory)
    for source, shader_type in zip(shader_sources, shader_types):
        source = current_directory + '\\' + source
        with open(source, 'r') as file:
            shader_source = file.read()
            shader = compileShader(shader_source, shader_type)
            shaders.append(shader)

    program = compileProgram(*shaders)

    return program

def ConstProgram(shader_sources, shader_type):

    shaders = []
    for shader_source,shader_type in zip(shader_sources,shader_type):
        shader = compileShader(shader_source, shader_type)
        #check compoile status
        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if status != GL_TRUE:
            raise RuntimeError(glGetShaderInfoLog(shader))
        shaders.append(shader)
    
    program = compileProgram(*shaders)
    return program

#uniforms

def glSetInt(program, name, value):
    location = glGetUniformLocation(program, name)
    if(location == -1):
        raise RuntimeError("Uniform not found")
    
    
    glUniform1i(location, value)

def glSetVec4(program, name, value):
    location = glGetUniformLocation(program, name)
    if(location == -1):
        raise RuntimeError("Uniform not found")
    
    glUniform4fv(location, 1, value)

def glSetVec2(program, name, value):
    location = glGetUniformLocation(program, name)
    if(location == -1):
        raise RuntimeError("Uniform not found")
    
    glUniform2fv(location, 1, value)

def glSetFloat(program, name, value):
    location = glGetUniformLocation(program, name)
    if(location == -1):
        raise RuntimeError("Uniform not found")
    
    glUniform1f(location, value)

def glSetBlock(program, name, value):
    
    location = glGetUniformBlockIndex(program, name)
    if(location == -1):
        raise RuntimeError("Uniform not found")
    glUniformBlockBinding(program, location, value)

# meshes
    
class simple_element_mesh:

    def __init__(self):

        self.vertex_array = glGenVertexArrays(1)
        self.vertex_buffer = glGenBuffers(1)
        self.element_buffer = glGenBuffers(1)

    def update(self, vertex_data, element_data, layout, layout_size):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, element_data.nbytes, element_data, GL_STATIC_DRAW)
        return

    def init_buffers(self, vertex_data, element_data, layout, layout_size):
    
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, element_data.nbytes, element_data, GL_STATIC_DRAW)

        type_memory_map = {
            GL_FLOAT: 4,
            GL_UNSIGNED_INT: 4
        }
        
        memory_covered = 0
        for i in range(0, len(layout)):
            spread = layout[i][0]
            data_type = layout[i][1]

            glEnableVertexAttribArray(i)
            glVertexAttribPointer(i, spread, data_type, GL_FALSE, layout_size, ctypes.c_void_p(memory_covered))
            memory_covered += spread*type_memory_map[data_type]

    def bind_for_draw(self):
        glBindVertexArray(self.vertex_array)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.element_buffer)

        return

class simple_element_geometry:

    def __init__(self):

        self.vertex_data = np.array([], dtype=np.float32)
        self.element_data = np.array([], dtype=np.uint32)

        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0

        return
    
    def resize_arrays(self, n, relations):
        
        self.vertex_data.resize(n*relations[0], refcheck=False)
        self.element_data.resize(n*relations[1], refcheck=False)
        return
    
    def reset_indexes(self):
        self.vertex_index = 0
        self.element_index = 0
        self.current_element = 0
        return
    
    def append_vec4(self, x,y,z,w):

        self.vertex_data[self.vertex_index] = x
        self.vertex_data[self.vertex_index+1] = y
        self.vertex_data[self.vertex_index+2] = z
        self.vertex_data[self.vertex_index+3] = w

        self.vertex_index += 4

        return
    
    def append_element_tri(self, a,b,c):

        self.element_data[self.element_index] = self.current_element+a
        self.element_data[self.element_index+1] = self.current_element+b
        self.element_data[self.element_index+2] = self.current_element+c

        self.element_index += 3
        self.current_element += 3

        return
    
    def append_element_quad(self, a,b,c,d):
        self.element_data[self.element_index] = self.current_element+a
        self.element_data[self.element_index+1] = self.current_element+b
        self.element_data[self.element_index+2] = self.current_element+c

        self.element_data[self.element_index+3] = self.current_element+a
        self.element_data[self.element_index+4] = self.current_element+d
        self.element_data[self.element_index+5] = self.current_element+c

        self.element_index += 6
        self.current_element += 4

        return
