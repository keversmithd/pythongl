import glfw

# currently ecompasses window information, texture units, should include buffer units, mouse information, scoped time information, and houses event objects.

# god class anti pattern

# only realisitc solution to provide a wrapper like state or a context which has sub objects for each class type.
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

        # set up render_batch like a list of objects to call render on, could just store a pointer to the draw call but doesn't work quite as well in lower level languages.
        
        # might need to stop rendering this thing so keep as map for now.

        # another concern is it might be better to package a mesh which includes the geometry and material but which limits the on draw behaviour, so this is a temporary thing.

        # reusable pattern
        # returns index into render batch based on id.
        self.render_batch_id = {}
        # array of render cells which can be nothing so they don't render.
        self.render_batch = []
        # array of reusable cells in the render batch to borrow.
        self.available_render_batch_cells = []

        self.event_objects = []

        return

    def attach_window(self, window):
        self.window = window
        window_size = glfw.get_window_size(window)
        
        self.vw = window_size[0]
        self.vh = window_size[1]
        return

    # adds object to render_batch
    def add_render(self, obj, id=None):
        
        if ( len ( self.available_render_batch_cells ) > 0 ):
            # get available cell id
            cell_id = self.available_render_batch_cells.pop( )
        else:
            # generate a new cell id 
            cell_id = len ( self.available_render_batch_cells )
            self.render_batch.append(obj)
        
        # if id is not preseneted then set id to string of cell id for automatic removal, and return the cell_id.
        if ( id  == None ):
            self.render_batch_id[ str(cell_id) ] = cell_id
            return str(cell_id)
        else:
            # else if there is an id set the id to the cell id and return it.
            self.render_batch_id[ id ] = cell_id
            return(id)

    # void removes the render list call if it exists.
    def remove_render(self, id):

        if ( id in self.render_batch_id ):
            # get the cell id 
            cell_id = self.render_batch_id[id]
            # set object to none in the array
            self.render_batch[cell_id] = None
            self.available_render_batch_cells.append(cell_id)

            return
        else:
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
    