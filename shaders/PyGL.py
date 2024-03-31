from PyGLHelper import *

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

def initWindow():
    if not glfw.init():
        return

    DebugOutput = True
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
    if(DebugOutput == True):
        glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, GL_TRUE)
    # Create a window
    window = glfw.create_window(800, 600, "OpenGL Window", None, None)
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


    return window

def main():
    # Initialize GLFW
    window = initWindow()
    program = CreateProgram(["shaders/test.vs", "shaders/test.fs"], [GL_VERTEX_SHADER, GL_FRAGMENT_SHADER])
    
    glClearColor(0.0, 1.0, 0.0, 1.0)
    # Main loop
    while not glfw.window_should_close(window):
        # Clear the buffer
        glClear(GL_COLOR_BUFFER_BIT)

        # Render your OpenGL scene here

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()


main()