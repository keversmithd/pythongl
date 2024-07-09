
class glml_node:
    parent = None
    element_title = None
    children = None
    attributes = None

    def __init__(self,element_title, attributes):

        if ( "display" not in attributes ):
            attributes["display"] = "block"

        self.attributes = attributes
        self.element_title = element_title
        self.textContent = ""
        self.children = []
        self.hasText = False

        

        # store internal state information regarding sizing, padding, layout and offset
        
        return

class glml_parse_state:

    def __init__(self, parse_index, parsing_content):

        self.parse_index = parse_index

        self.parsing_content = parsing_content
        self.parsing_content_length = len(parsing_content)

        # end of the parsing meta context

        # attributing node
        self.current_element_title = None
        self.currently_attributing_element = None
        self.last_attributing_element = None

        # may want the tree to be a node
        self.root = None
        self.current_node = None

        # map of defaults 
        self.node_defaults = {
            "display" : "block"
        }

        return

def close_element(state_ptr):
    
    state = state_ptr[0]
    # so if using a tree this is when we make the attributing element the parent of the 
    # current node
    if(state.root == None):
        print("Error no root no open element")
    else:
        if(state.current_node.parent != None):
            state.current_node = state.current_node.parent

    return

def enlist_element(state_ptr):
    
    state = state_ptr[0]
    # so if using a tree this is when we make the attributing element the parent of the 
    # current node
    if(state.root == None):
        state.root = glml_node(state.current_element_title, state.currently_attributing_element)
        state.current_node = state.root
    else:
        # create the new node
        node = glml_node(state.current_element_title, state.currently_attributing_element)
        # set the nodes parent to the current node
        node.parent = state.current_node
        state.current_node.children.append(node)
        state.current_node = node
    return

def recognize_element(element_title, state_ptr):

    recognized_elements = {"el":0}
    recognized_attributes = {0: {"box":["","","",""],"width":"","height":"","color":["","","",""],"id":"", "text":"", "display": "block"} }

    state = state_ptr[0]

    if( element_title in recognized_elements ):
    
        element_index = recognized_elements[element_title]
        
        element_attributes = recognized_attributes[element_index]
        state.currently_attributing_element = element_attributes.copy()
        state.current_element_title = element_title

        return True
    else:
        return False

def get_attribute_parameter(attribute_title, state_ptr):
    state = state_ptr[0]
    # assumed to of stopped at the equals sign and now we want to parse the information
    state.parse_index += 1
    attributing_element = state.currently_attributing_element


    # model absorb things between common delimiters
    acceptable_open_delimeters = {"{", "(", "\""}
    acceptable_close_delimeters = {"}",")", "\""}
    acceptable_element_delimeters = {","}

    open = False

    attribute_index = 0

    # Indicates the attribute is singular and not an array
    singular = False

    if (state.parsing_content[state.parse_index] in acceptable_open_delimeters and state.parsing_content[state.parse_index] in acceptable_close_delimeters ):
        state.parse_index += 1
        singular = True
        
        open = True

        if ( attribute_title in state.node_defaults ):
            state.currently_attributing_element[attribute_title] = ""

    

    while( state.parse_index < state.parsing_content_length and state.parsing_content[state.parse_index] not in acceptable_close_delimeters ):
        
        if ( state.parsing_content[state.parse_index] in acceptable_element_delimeters ):
            attribute_index += 1
        elif ( state.parsing_content[state.parse_index] in acceptable_open_delimeters and open == False):
            open = True
        elif ( singular == False and open == True and attribute_title in state.currently_attributing_element ):
            state.currently_attributing_element[attribute_title][attribute_index] += state.parsing_content[state.parse_index]
        elif ( open == True and attribute_title in state.currently_attributing_element and singular == True ):
            state.currently_attributing_element[attribute_title] += state.parsing_content[state.parse_index]
            singular = True
       
        
        state.parse_index += 1

    # go past close delimiter.


    return

def get_attribute_title(state_ptr):
    # unpack ptr
    state = state_ptr[0]    

    stop_tokens = {" ", "=", "(", ")", "/", ">"}

    #strip leading white space
    while ( state.parse_index < state.parsing_content_length and state.parsing_content[state.parse_index] == " "):
        state.parse_index += 1
    
    attribute_title = ""
    token_stopped_at = ""
    while ( state.parse_index < state.parsing_content_length ):
        token = state.parsing_content[state.parse_index]
        if(token in stop_tokens):
            token_stopped_at = token
            break
        attribute_title += token
        state.parse_index += 1

    return attribute_title, token_stopped_at

def eat_closing_tag(state_ptr):
    state = state_ptr[0]
    state.parse_index += 1
    potential_element_title, token_stopped_at = get_attribute_title(state_ptr)

    while(state.parse_index < state.parsing_content_length):

        attribute_title, token_stopped_at = get_attribute_title(state_ptr)
        if(token_stopped_at == ">"):
            state.parse_index += 1
            break
        if(token_stopped_at == "="):
            #get_attribute_parameter(attribute_title, state_ptr)
            #should try and eat the paramter, this is basically an error
            continue

        state.parse_index += 1

    return

def parse_element(state_ptr):
    # parse all attributes up until the closing bracket, and if / is found then end current element attribution.

    # first we want to strip the leading white space if there is any after the cone
    # then absorb all tokens up to the white space for the title of the element
    # =" and ( if we encounter these characters before a space then there is not element name default to el

    state = state_ptr[0]
    
    #get rid of the open brack slash
    state.parse_index += 1

    potential_element_title, token_stopped_at = get_attribute_title(state_ptr)

    if ( token_stopped_at == "/"):
        # if there is the slash in the preamble then please close the current element, i guess disregard the name
        # for now
        close_element(state_ptr)
        
        eat_closing_tag(state_ptr)
        
        return
        
    else:
        if ( not recognize_element(potential_element_title, state_ptr) ) : recognize_element("el", state_ptr)

    # after this we want to get more attribute titles and then absorb their content
    while(state.parse_index < state.parsing_content_length):

        attribute_title, token_stopped_at = get_attribute_title(state_ptr)
        if(token_stopped_at == ">"):
            enlist_element(state_ptr)
            state.parse_index += 1
            break
        if(token_stopped_at == "="):
            get_attribute_parameter(attribute_title, state_ptr)

        state.parse_index += 1

    return

def handle_token(state_ptr):
    # unpack ptr
    state = state_ptr[0]

    unit_token = state.parsing_content[state.parse_index]

    special_characters = {"<":parse_element}
    restricted_tokens = {"\n", "\t"}

    if ( unit_token in special_characters ):
        special_characters[unit_token](state_ptr)
    else:
        #add text content to the current attributing node
        if(state.currently_attributing_element != None and state.current_node != None and unit_token not in restricted_tokens):

            # determine if the current node has text or not
            if ( unit_token != ' '):
                state.current_node.hasText = True

            state.current_node.textContent += unit_token
        state.parse_index += 1
    
    return

def parse_glml(ui):
    
    #set parse state
    state = glml_parse_state(0, ui)

    # set the root as the god node
    state.root = glml_node("god", {})
    state.current_node = state.root

    # text length
    while(state.parse_index < state.parsing_content_length):

        handle_token([state])

        #state.parse_index += 1

    return state

def print_attributes(node):
    
    for attr in node.attributes:
        
        print(attr, ": ", node.attributes[attr])
            
def traverse_state(root):
    
    if (root == None):
        return

    print_attributes(root)

    for child in root.children:
        
        traverse_state(child)


# glml_token = parse_glml('''
# <el box=(1,1,1,1)>Parent
#     <el id="mode">Child</>
#     <el>Second Child</>
# </>''')


        
    
