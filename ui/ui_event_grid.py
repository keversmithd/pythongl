import os
import sys
import random

workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)

from shaders.PyGLHelper import *
from state.state import *

# event grid



class event_grid():
    
    def __init__(self):
        
        # resolution of the grid over the normalized domain
        self.resolutionX = 10
        self.resolutionY = 10

        return
    
    



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
    
    glClearColor(1.0, 1.0, 0.0, 1.0)

    
    # Main loop
    while not glfw.window_should_close(window):
        # Clear the buffer
        glClear(GL_COLOR_BUFFER_BIT)
        
        scene.time = glfw.get_time()

        # Swap buffers and poll events
        glfw.swap_buffers(window)
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()


main()