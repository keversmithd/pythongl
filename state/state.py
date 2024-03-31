import glfw
class state:
    def __init__(self):

        self.texture_atlases = {}
        self.used_texture_units = 0


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
        self.vh = window_size[0]
        self.vw = window_size[1]

        return
    
    def on_key_event(self, key, scancode, action, mods):
        for event_object in self.event_objects:
            if(event_object.on_key_event != None):
                event_object.on_key_event(key, action)
        return

    def on_mouse_move(self, x,y):
        self.mx = x
        self.my = y
        
        

        #update mouse event for objects
        for event_object in self.event_objects:
            event_object.on_mouse_move(x,y)

        return
    
    