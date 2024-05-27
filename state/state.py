import glfw

class state:
    def __init__(self):

        #texture related
        self.texture_atlases = {}
        self.used_texture_units = 0

        #buffer related
        self.used_uniform_buffers = 0


        self.window = None
        self.vw = 0
        self.vh = 0

        #mouse related callbacks
        self.mx = 0
        self.my = 0

        #time related
        self.time = 0

        self.event_objects = []

        return
    
    def attach_window(self, window):
        self.window = window
        window_size = glfw.get_window_size(window)
        
        self.vw = window_size[0]
        self.vh = window_size[1]
        return
    
    def on_key_event(self, key, scancode, action, mods):
        
        # rough event detection
        for event_object in self.event_objects:
            if(hasattr(event_object, 'on_key_event') and event_object.on_key_event != None):
                event_object.on_key_event(key, action)
        return

    def on_mouse_move(self, x,y):
        self.mx = x
        self.my = y
        
        

        #update mouse event for objects
        for event_object in self.event_objects:
            if(hasattr(event_object, 'on_mouse_move') and event_object.on_mouse_move != None):
                event_object.on_mouse_move(x,y)

        return

    def on_left_click(self, button, action, mods):
        for event_object in self.event_objects:
            if(hasattr(event_object, 'on_left_click') and event_object.on_left_click != None):
                event_object.on_left_click()
        return

    def add_uniform_buffer(self):
        self.used_uniform_buffers += 1
        return self.used_uniform_buffers-1
    