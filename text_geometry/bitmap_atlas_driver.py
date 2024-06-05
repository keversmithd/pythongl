import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *
from bitmap_atlas import *
from state.state import *
from bitmap_text import *
from text_display_box import *
from ui.layout_element import *


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

def mouse_button_call(window, button, action, mods):
    scene = glfw.get_window_user_pointer(window)
    
    if(action == glfw.PRESS):
        if(button == glfw.MOUSE_BUTTON_LEFT):
            scene.on_left_click(button, action, mods)
    
    return

def window_setup(window, state):

    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_BLEND)

    state.attach_window(window)

    glfw.set_cursor_pos_callback(window, mouse_call)
    glfw.set_key_callback(window, key_call)
    glfw.set_mouse_button_callback(window, mouse_button_call)

    return

def main():
    # Initialize GLFW

    scene = state()
    window = initWindow(800,600, True, "Hello world", window_setup, scene)
    if not window:
        return  
    
    # setting state
    glfw.set_window_user_pointer(window, scene)
    
    #Loading singular font
    joanRegularAtlas = bitmap_atlas_loader("fonts\\Joan-Regular.ttf", [512,512], 10, 10).make_atlas(scene, "joanRegular")
    
    #Simple bitmap font generator
    #text_maker = bitmap_text(scene)
    #text_maker.render_text("hellog", "joanRegular")

    tracked_value = ["track mgggml"]
    tracked_text_display = text_display(scene, "joanRegular")

    tracked_text_display.set_tracked_value(tracked_value)
    tracked_text_display.set_location(np.array([-1.0,0.0], dtype=np.float32))
    tracked_text_display.set_container( [ np.array([0,0.0], dtype=np.float32), np.array([1,1], dtype=np.float32) ] )
    tracked_text_display.set_size(3)

    tracked_text_display.generate_mesh()

    ui = """

    <el id="toolbar" box = (-1vw,0,1vw,0) height = 20px color = (1,0,0,1)>
        <el id="File Button"> File </el>
    </el>

    how responsive is this portal montior, thank you richard for becoming
    a citizen of the monto space.

    <el id="footbar" box = (-1vw,-1vw, 1vw, -1vw) height = 20px color = (1,0,0,1)>
    </el>

    """

    parent_element = layout_element(scene)
    parent_element.set_style((0.5,0.5,1.0,1.0), (1,0,0,1), 0)
    child_element  = layout_element(scene, parent_element)
    child_element.set_style((0.0,0.0, 1.0,1.0), (0,1,0,1), 1)



    glClearColor(1.0, 1.0, 0.0, 1.0)

    
    # Main loop
    while not glfw.window_should_close(window):
        # Clear the buffer
        glClear(GL_COLOR_BUFFER_BIT)
        
        scene.time = glfw.get_time()

        parent_element.render()
        #child_element.draw()
        # Render your OpenGL scene here
        #tracked_text_display.draw()
        

        if(glfw.get_key(window, glfw.KEY_V) == glfw.PRESS):
            tracked_value[0] = "track" + random.choice(["me", "you", "us", "them"])

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

main()