
class mouse_helper:


    def __init__(self, state):
        state.event_objects.append(self)
        return
    
    def on_mouse_move(self,x,y):
        return