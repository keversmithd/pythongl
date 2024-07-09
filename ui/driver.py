import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)
from shaders.PyGLHelper import * 

from state.state import *
from ui.layout_element_machine import *
# Load the bitmap loader
from text.bitmap_atlas_loader import *
# and the text machine
from text.text_machine import *
# import cube geometry
from meshes.cube_geometry import *
from shaders.BasicMaterial import *
from shaders.BasicMesh import *
from cameras.PerspectiveCamera import *

# import the glml transformer object
from ui.transform_glml import *

def mouse_call(window, x,y):
    scene = glfw.get_window_user_pointer(window)
    scene.on_mouse_move(x,y)
    
    return

def key_call(window, key, scancode, action, mods):
    scene = glfw.get_window_user_pointer(window)
    scene.on_key_event(key, scancode, action, mods)

    if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    return


def window_setup(window, state):

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    glEnable(GL_BLEND)
    state.attach_window(window)

    glfw.set_cursor_pos_callback(window, mouse_call)
    glfw.set_key_callback(window, key_call)

    return

# updates context objects inside of the current state
def create_context(scene):

    # Load a generic bitmap to be used
    bitmap_atlas_loader(scene, "joan", "fonts\\Joan-Regular.ttf")

    # Setup the instance text machine
    scene.add_element_machine( layout_element_machine(scene) )
    scene.add_text_machine ( text_machine(scene, "joan") )

def main():
    # Initialize GLFW 

    scene = state()
    window = initWindow(800,600, True, "Hello world", window_setup, scene)
    if not window:
        return  

    # setting state
    glfw.set_window_user_pointer(window, scene)
    
    # set up the scene context with context objects
    create_context(scene)

    # Add the camera to the
    camera = PerspectiveCamera( scene )
    scene.add_camera(camera, "fps")

    # text_obj = text("hello")
    # text_obj.location = [-1, -0.9]
    # limiting_container = [-1, -1, 1, 1]

    # scene.text_machine.push_text(text_obj, limiting_container, True)


    # style = layout_style()
    # style.container = (container[0], container[1], container[2], container[3])
    # style.relation = (0,0,0,0)

    #scene.element_machine.push_element(style)
    
    transformer = transform_glml(scene)
    transformer.render('''
    <el display="inline" width="0.3">
        <el display="inline">Hello</>
        <el>Goodbyea</>
        <el>Hello</>
        <el>Goodbye</>
    </el>
    <el>Below</>

    ''')

    # Load a clear color.
    glClearColor(0.0, 0.0, 0.0, 1.0)
    
    # Main loop
        # Clear the buffer
    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
    
        scene.update_time( glfw.get_time() )

        scene.render()

        if ( glfw.get_key(scene.window, glfw.KEY_SPACE ) ):
            to.set_text("in")
            to.set_position([-0.1,0.0])

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

main()