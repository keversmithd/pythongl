
import math
import numpy as np
# Takes document tree and applies the same principle as the glml transformer but applies it to the bases of the frustrum

# use seperate build info class and share for future correctness.

class frustrum_build_info:

    def __init__(self, width, height, container):

        self.width = width
        self.height = height
        self.container = container
        self.offset_x = 0
        self.offset_y = 0

class frustrum_ui:

    def __init__(self, state):

        # set the state up correctly.
        self.state = state

        # define the global container
        self.global_container = [0,0,1,1]

        # map for how to handle pre offsets based on display
        self.pre_offset_map = {
            "block" : self.pre_block_offset,
            "inline" : self.pre_inline_offset,
        }

        # map for how to handle post offsets based on display
        self.post_offset_map = {
            "block" : self.post_block_offset,
            "inline" : self.post_inline_offset,
        }

        # define the frustrum details
        self.frustrum_origin = None
        self.frustrum_right = None
        self.frustrum_up = None

        # define the frustrum in terms of its big boy status.
        self.update_frustrum()

        

        return

        
    # update the frustrum.
    def update_frustrum(self):  

        if ( self.state.active_camera == None ):
            return

        if ( self.state.active_camera.projection_type == "Perspective" ):

            # get the projective attributes from the camera
            fov = self.state.active_camera.fov
            near = self.state.active_camera.near_plane
            
            # get the aspect ratio
            a = self.state.active_camera.aspect_ratio

            # find
            tanHalfFov = math.tan( math.radians(fov/2) )

            halfWidth = (tanHalfFov*near)
            halfHeight = halfWidth*a

            forward = self.state.active_camera.forward
            forward = forward/np.linalg.norm(forward)
            right = np.cross( forward, self.state.active_camera.up )
            right = right/np.linalg.norm(right)
            up = np.cross( forward, right )
            up = up/np.linalg.norm(up)

            camera_position = self.state.active_camera.position

            frustrum_origin = np.add ( camera_position, forward*near )
            frustrum_origin = np.subtract (frustrum_origin, right*halfWidth )

            self.frustrum_origin = np.add ( frustrum_origin, up*halfHeight )

            self.frustrum_width = halfWidth*2.0
            self.frustrum_height = halfHieght*2.0

            self.frustrum_up = up
            self.frustrum_right = right

    def transform( self, document_tree ):
        # traverse document_tree
        # creating elements in scene_context at each node
        # and then just setting the previous parent as the attribute.

        root = document_tree.root
        # check if the root is null
        if ( root == None ):
            print("FRUSTRUM_UI: Bad root")
            return

        # create a god node and set the roots parent as this.
        self.depth_build( root )

            
        return


    # determine the pre container, calculated height, calculated width etc.
    def pre_container(self,node):

        # if the root is present
        if ( node.parent == None ):
            # if internal width is set
            width = 0.0
            height = 0.0

            # calculate the mask container change the mask container depending on anchor
            mask_container = [0,0,1,1]

            # calculate the dx and dy of the parent container.
            pdx = self.global_container[2] - self.global_container[0]
            pdy = self.global_container[3] - self.global_container[1]

            if ( "width" in node.attributes ):
                width = node.attributes["width"]

                mask_container[0] = 0
                mask_container[2] = 0

            if ( "height" in node.attributes ):
                height = node.attributes["height"]

                mask_container[1] = 0
                mask_container[3] = 0

            if ( "box" in node.attributes ):
                box = node.attributes["box"]
                mask_container[0] = float ( box [0] )
                mask_container[1] = float ( box [1] )
                mask_container[2] = float ( box [2] )
                mask_container[3] = float ( box [3] )

                width = 0.0
                height = 0.0

            # calculate the location present
            lx = 0.0
            ly = 0.0

            if ("position" in node.attributes ):
                lx = float ( node.attributes["position"][0] )
                ly = float ( node.attributes["position"][1] )
            
        
            
            # initialize the calculated container
            node.calculated_container = [0,0,0,0]

            # update calculated container
            node.calculated_container[0] = self.global_container[0] + (lx*pdx) + (mask_container[0]*pdx)
            node.calculated_container[1] = self.global_container[1] + (ly*pdy) + (mask_container[1]*pdy)
            node.calculated_container[2] = self.global_container[0] + (lx*pdx) + (mask_container[2]*pdx) + (width*pdx)
            node.calculated_container[3] = self.global_container[1] + (ly*pdy) + (mask_container[3]*pdy) + (height*pdy)

            # set up the container offset to be
            node.calculated_offset = [0,0]

            node.calculated_width = node.calculated_container[2]-node.calculated_container[0]
            node.calculated_height = node.calculated_container[3]-node.calculated_container[1]

        else:

            # retrieve the parent container
            parent_container = node.parent.calculated_container

            # if internal width is set
            width = 0.0
            height = 0.0

            # calculate the mask container change the mask container depending on anchor
            mask_container = [0,0,1,1]

            if ( node.attributes["width"] != "" ):
                width = float ( node.attributes["width"] )

                mask_container[0] = 0
                mask_container[2] = 0

            if ( node.attributes["height"] != "" ):
                height = float ( node.attributes["height"] )

                mask_container[1] = 0
                mask_container[3] = 0

            if ( node.attributes["box"] != ["","","",""] ):
                box = node.attributes["box"]
                mask_container[0] = float ( box [0] )
                mask_container[1] = float ( box [1] )
                mask_container[2] = float ( box [2] )
                mask_container[3] = float ( box [3] )

                width = 0.0
                height = 0.0

            # calculate the location present
            lx = 0.0
            ly = 0.0

            if ("position" in node.attributes ):
                lx = float ( node.attributes["position"][0] )
                ly = float ( node.attributes["position"][1] )
            
            
            ox = node.parent.calculated_offset[0]
            oy = node.parent.calculated_offset[1]
        
            # calculate the dx and dy of the parent container.
            pdx = (node.parent.calculated_container[2] - node.parent.calculated_container[0])
            pdy = (node.parent.calculated_container[3] - node.parent.calculated_container[1])

            # update calculated node height as sub portion of the parent container
            node.calculated_width = width*pdx
            node.calculated_height = height*pdy

            # initialize the calculated container
            node.calculated_container = [0,0,0,0]

            # update calculated container
            node.calculated_container[0] = node.parent.calculated_container[0] + (lx*pdx) + (ox) + (mask_container[0]*pdx)
            node.calculated_container[1] = node.parent.calculated_container[1] + (ly*pdy) + (mask_container[1]*pdy)
            node.calculated_container[2] = node.parent.calculated_container[0] + (lx*pdx) + (mask_container[2]*pdx) + (width*pdx)
            node.calculated_container[3] = node.parent.calculated_container[1] + (ly*pdy) - (oy) + (mask_container[3]*pdy) + (height*pdy)
        
            # initialize the inner offset
            node.calculated_offset = [0,0]

            node.calculated_width = node.calculated_container[2]-node.calculated_container[0]
            node.calculated_height = node.calculated_container[3]-node.calculated_container[1]

    # determine the pre padding, assumes all padding elements are present.
    def pre_padding(self,node):

        
        if ( "padding" in node.attributes ):
            padding = node.attributes["padding"]
            px = float (  padding[0]  )
            py = float (  padding[1]  )
            pz = float (  padding[2]  )
            pw = float (  padding[3]  )
        else:
            px = 0.0
            py = 0.0
            pz = 0.0
            pw = 0.0

        width = node.calculated_width
        height = node.calculated_height

        # create the calculated container container
        node.calculated_contained = [0,0,0,0]

        # change the calculated container space
        node.calculated_contained[0] = node.calculated_container[0] + width*px
        node.calculated_contained[1] = node.calculated_container[1] + height*py
        node.calculated_contained[2] = node.calculated_container[2] + width*pz
        node.calculated_contained[3] = node.calculated_container[3] + height*pw

        # update the base offset of padding
        node.calculated_offset[0] = px*width
        node.calculated_offset[1] = py*width

        # setup the calculated padding
        node.padding = [ px,py,pz,pw ]

    # add element background rendering
    def add_background_content(self, node):

        # generate the layout style
        style = layout_style()
        style.relation = (0,0,0,0)
        style.container = ( node.calculated_contained[0], node.calculated_contained[1], node.calculated_contained[2], node.calculated_contained[3] )
        style.parent_container = ( self.global_container[0], self.global_container[1], self.global_container[2], self.global_container[3] )
        
        # push the style to the element machine
        self.state.element_machine.push_element(style)

    # render the text at the current offset of the current node
    def render_text(self, node):

        if ( node.hasText == False ):
            return [0,0,0,0]


        if ( node.parent != None ):

            # retrieve relative offset of the parent to place the text.
            off_x = node.parent.calculated_offset[0]
            off_y = node.parent.calculated_offset[1]

            text_obj = text(node.textContent)
            text_obj.location[0] = node.parent.calculated_container[0] + off_x
            text_obj.location[1] = node.parent.calculated_container[3] - off_y

            limiting_container = node.parent.calculated_contained

            text_box = self.state.text_machine.push_text(text_obj, limiting_container, True)
            return text_box
        else:
            # retrieve relative offset of the parent to place the text.
            off_x = node.calculated_offset[0]
            off_y = node.calculated_offset[1]

            text_obj = text(node.textContent)
            text_obj.location[0] = node.calculated_container[0] + off_x
            text_obj.location[1] = node.calculated_container[3] + off_y
            limiting_container = node.calculated_contained

            text_box = self.state.text_machine.push_text(text_obj, limiting_container, True)
            return text_box

    

    # generates the build info based on the content size box and node
    def pre_build_info(self, node, content_box):

        off_x = content_box[2]
        off_y = content_box[3]

        content_width = content_box[2]-content_box[0]
        content_height = content_box[3]-content_box[1]

        info = build_info(content_width, content_height, [ content_box[0], content_box[1], content_box[2], content_box[3]] )

        if ( node.parent == None ):
            return info

        info.offset_x = content_width
        info.offset_y = content_height

        # if the box is set then just update the offset and do not alter the width and height 
        # if ( node.attributes["box"] != ["","","",""] ):
        #     return info
        # if ( node.attributes["width"] != "" ):
        #     # update the calculated_container of the internal node
        #     node.calculated_container[2] = node.calculated_container[0]+content_width
        #     info.width = content_width    
        # if ( node.attributes["height"] == "" ):
        #     node.calculated_container[3] = node.calculated_container[1]+content_height
        #     info.height = content_height

        return info
            
    # update pre offsets based on node type
    def pre_block_offset(self, node, build_info):
        node.calculated_offset[0] = node.padding[0]*node.calculated_width
        node.calculated_offset[1] += build_info.offset_y

    # inline pre offset
    def pre_inline_offset(self, node, build_info):
        node.calculated_offset[0] += build_info.offset_x
        node.calculated_offset[1] = node.padding[1]*node.calculated_height

    # update the offsets of the current node based build info
    def post_block_offset(self, node, build_info):

        # reset the x offset and increment by the y offset
        node.calculated_offset[0] = node.padding[0]*node.calculated_width
        node.calculated_offset[1] +=  build_info.offset_y

        return

    # inline post offset
    def post_inline_offset(self, node, build_info):

        node.calculated_offset[0] += build_info.offset_x
        node.calculated_offset[1] = node.padding[1]*node.calculated_height

        return

    # expand the content info based on the child build
    def expand_content_info(self, build_info, child_build_info):

        build_info.container[0] = min(build_info.container[0], child_build_info.container[0])
        build_info.container[1] = min(build_info.container[0], child_build_info.container[1])
        build_info.container[2] = max(build_info.container[0], child_build_info.container[2])
        build_info.container[3] = max(build_info.container[0], child_build_info.container[3])

        build_info.width = max(build_info.width, child_build_info.width)
        build_info.height = max(build_info.height, child_build_info.height)

        build_info.offset_x += child_build_info.width
        build_info.offset_y = build_info.height

    # post update update the container, with the content height of the node after being built.
    def depth_build(self,node):

        # set up the pre container which sets the bounding box, width/height
        self.pre_container(node)
        # set up the pre padding which updates the post calc bounding box and updates the offset
        self.pre_padding(node)

        # render the text content of the node
        content_box = self.render_text(node)

        # generate the build info for this node
        content_info = self.pre_build_info(node, content_box) 

        # then update the offset depending on display of the node
        self.pre_offset_map[ node.attributes["display"] ](node, content_info)

        # create the element style based on the node.
        #self.add_background_content(node)

        for c in range(0, len(node.children)):

            # pre fill padding, container, and
            child_build_info = self.depth_build( node.children[c] )

            # extend the content_info based on the child_build_info
            self.post_offset_map[ node.attributes["display"] ](node, child_build_info)

            # expand the current content info 
            self.expand_content_info( content_info, child_build_info )

            # post update the container and padding.

        # expand the parent offsets

        return content_info



            




