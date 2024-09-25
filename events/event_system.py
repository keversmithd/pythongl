
import numpy as np
import os
import sys
import ctypes


workspace_directory = os.path.dirname(os.path.realpath(__file__))
workspace_directory = workspace_directory.rsplit('\\', 1)[0]
sys.path.append(workspace_directory)



from data_structures.segment_tree.interval_segment_tree import *

# assume some wrapper object, which opens interfaces to the object
# but also should have access to certain instancing machines.

# EVENT SYSTEM
class EventSystem :

    def __init__( self, state ):
        self.state = state
        self.event_tree = interval_segment_tree (  )

        # store the last event issued
        self.last_event = None

        # store the timeline head
        self.timeline_head = 0.0

        # time line end
        self.timeline_end = 0.0

        # Store the animateable attributes
        self.animateable_attributes = {
            "position" : self.update_position
        }

        # Store the retrievable attributes
        self.retrieveable_attributes = {
            "position" : self.get_position
        }

        # Store the easing methods 
        self.easing_methods = { 
            "linear" : self.lerp
        }

    # interpolators
    def lerp(self, a,b, t):

        return ((1-t)*a) + (t*b)

    # getters and setters

    def get_position ( self, event_head, event_attribute ):

        event_attribute["from"] = event_head["object"].get_position()
    
    def update_position ( self, event_head, event_attribute, t ):



        fro = event_attribute["from"]
        to = event_attribute["to"]

        x = self.easing_methods[ event_attribute["easing"] ] ( fro[0], to[0], t )
        y = self.easing_methods[ event_attribute["easing"] ] ( fro[1], to[1], t )
        z = self.easing_methods[ event_attribute["easing"] ] ( fro[2], fro[2], t )

        event_head["object"].set_position ( x,y,z )

    # Adds the event into the event tree in the format of  ( head , [args])
    def timeline_insert ( self, event_head, event_arguments ):

        # define the segment
        event_segment = ( event_head["start"], event_head["end"] )
        
        # The event value should be maybe a tuple??
        event_value = ( event_head, event_arguments )

        # insert into the tree
        self.event_tree.insert( event_segment, event_value ) 

    # helper function to sort out an undefined head
    def sort_head (self, head):

        # If the object is not in the head
        if ( "object" not in head ):
            return False

        if ( "still" in head and self.last_event != None):
            head["start"] = self.last_event.start
        elif ( "start" not in head ):
            head["start"] = self.timeline_end

        # Update the regional bounds of the event.
        if ( "duration" in head ):
            head["end"] = head["start"] + head["duration"]
        elif ( "end" not in head ):
            return False

        return True

    # helper function to sort an arg into the valid arguments array
    def sort_arg ( self, arg ):

        if ( "to" not in arg ):
            return False
        if ( "attribute" not in arg ):
            return False
        
        if ( arg["attribute"] not in self.animateable_attributes ):
            return False

        # store the easing information
        if ( "easing" not in arg ):
            arg["easing"] = "linear"
        elif ( arg["easing"] not in self.easing_methods ):
            arg["easing"] = "linear"
        
        # set the from status of the arg machine
        if ( "from" not in arg ):
            arg["init"] = False
        else:
            arg["init"] = True
        
        return True
        
    # head { object:, start, end, }, {attributes}
    def add_event (self, head, *args ) :

        if  ( not self.sort_head ( head ) ) :
            return

        # Store the arguments
        arguments = []

        # Sort through args
        for arg in args:
            if ( self.sort_arg ( arg ) ):
                arguments.append( arg )
        
        # If any arguments made it through the sorting process then insert the event into the tree
        if ( len ( arguments) > 0 ):

            # update the greatest bound of the timeline end
            self.timeline_end = max ( self.timeline_end, head["end"])

            # insert the head and arguments into the timeline
            self.timeline_insert ( head, arguments )
        
    # handle event will find the t value into the current event and then act on the event attributes
    def handle_event ( self, event ):

        # find the t value
        t = ( self.timeline_head - event[0]["start"] )/( event[0]["end"] - event[0]["start"] )
        
        

        # iterate through the arguments to the event
        for a in range ( 0 , len ( event[1] ) ):

            # gather the event argument
            event_argument = event[1][a]

            # if the event has not been initiated in terms of its from value then initiate it.
            if ( event_argument["init"] == False ):

                # then retrieve the initiation of the event attributes
                self.retrieveable_attributes[ event_argument["attribute"] ]( event[0], event_argument )

                # then set init to true
                event_argument["init"] = True

            # the update the event argument with the updated t value
            self.animateable_attributes [ event_argument["attribute"] ]( event[0], event_argument, t )

    # updates events that are intersected by the current timeline head
    def update_events ( self ) :

        # attain the query results of the event nodes which intersect the timeline head.
        query_results = self.event_tree.query ( self.timeline_head )
        
        # iterate through the query results and then handle_event each event.
        for i in range ( 0, len ( query_results )): 
            self.handle_event ( query_results[i].value )
        return

    # update with the delta timeline to advance the timeline head
    def update( self, deltatime):

        

        # update events
        self.update_events()

        # increment the timeline head by delta time and and then update events
        self.timeline_head += deltatime 

            

# ev = EventSystem( { } )

# ev.add_event( { "object": "goodbye", "duration": 1 }, { "attribute": "position", "to": (1,1,1) } )
# ev.add_event( { "object": "hello", "duration": 1 }, { "attribute": "position", "to": (1,1,1) } )
    
# ev.update ( 0.5 )
# ev.update ( 0.5 )
# ev.update ( 0.5 )
# ev.update ( 0.5 )