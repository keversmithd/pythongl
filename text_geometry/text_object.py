from dtvb  import *
from text_triangles import *

class text_object:

    textGeometry = None
    dynamicTextBuffer = None

    chars = []

    def __init__(self,textGeometry,dynamicTextBuffer):
        self.textGeometry = textGeometry
        self.dynamicTextBuffer = dynamicTextBuffer

    def insert_text(self,text,position,orientation,color,scale, location=0):

        if(location == 0):
            location = len(self.chars)-1

        for i in range(0,len(text)):
            
            char_info = self.textGeometry.charmap[ord(text[i])] 
            if(char_info == None):
                
                continue
            char_buffer_id = self.dynamicTextBuffer.add_char(ord(text[i]),position,orientation,color,scale)

    def edit_char_char_code_at(self,location, new_char):

        #Gather char_buffer_id from the chars array.
        char_buffer_id = self.chars[location][0]
        dynamic_buffer_index = char_buffer_id*self.dynamicTextBuffer.char_attributes_float_size
        self.dynamicTextBuffer.char_buffer[dynamic_buffer_index] = new_char 

    def edit_char_with_parameters(self,location,parameters):

        char_buffer_id = self.chars[location][0]
        dynamic_buffer_index = char_buffer_id*self.dynamicTextBuffer.char_attributes_float_size

        for parameter_key,parameter_value in parameters.items():
            parameter_index = self.dynamicTextBuffer.parameter_map[parameter_key]

            if(parameter_key != "character" and parameter_key != "scale"):
                self.dynamicTextBuffer.char_buffer[dynamic_buffer_index+parameter_index] = parameter_value[0]
                self.dynamicTextBuffer.char_buffer[dynamic_buffer_index+parameter_index+1] = parameter_value[1]
                self.dynamicTextBuffer.char_buffer[dynamic_buffer_index+parameter_index+2] = parameter_value[2]
        



 
    

