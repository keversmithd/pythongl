# Euler vector

  get euler vector representation from axis angle
  https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula

  

# event system

  ## Key points


    ### Scene Object
      the scene object wraps around a pointer or self object, and interfaces are given to retrieve position, euler and quaternion.. etc
      if any of these are not available, then idk

      realistic usage:
        scene_object ( other_object? )
      
    ### Data structures

      event interval tree:

        MODEL AFTER A QUAD TREE.
          so the inital segment is the main segment, if a segement must be larger than this main segment then there 
          could be some form of rebuild that might be neccecary.
        

        insert event with region:
          moves down tree, searching sub trees of intersected segments, finds final leaf destination, if outside of the total range of the region tree, then reset tree with that new new domain  
        
      event hash list:

        MODEL AFTER A HASHTABLE
          # USE ARRAY OF LINKED LISTS THAT HASH OUT AS TIME SQUARES
        
        MODEL AFTER A SEGMENT TREE 
          # Build tree from ground up
          # Combine first two nodes into root
          # If inserted is larger than root, then make new root and combine the root and inserted
          # If inside of the root then travel down to the to the intersected leaf, then try to combine them.
          
    
    ### Usage
  

    

# glml transformer
  ## description:
    transforms glml text into the parsed tree and renders onto the screen.
  ## glml transformer algorithm
    depth first search, and updating inner parent offsets.
  ## Todo
    when the word wraps through push text in the textmachine, return information about the last location
    during the wrap and set the local offset to that location

# Layout elemement machine instanced
  layout_element_machine()
  .add_element({ container, parent_container, relation, color })
  ## to do
    border, stroke, opacity, etc.
# Text machine
  ideal usage
    text_id = text_machine.Text("text_machine1")
  ## wrapped text rendering
    how to define the line height, if the max height of the line is at unity 1.0, then everything there after is also larger.

#  Buffer geometry refactoring
  ## Element Buffers (Geometry | Buffer) in ElementBuffer.py
  interleaved works with customizations limited to simple index manipulation
  realistic usage:
    element_buffer = InterleavedElementBuffer({ "position": 0, "uvs": 1, "normals":3  })
    element_buffer.allocate(23) ; number of vertices
    InterleavedElementBuffer.push("type0"), InterleavedElementBuffer.push("type1"), InterleavedElementBuffer.push("type2")
    or
    InterleavedElementBuffer.push_all(["packed_data"])
    element_buffer.sync_buffers()
  ideal usage:
    element_buffer = InterleavedElementBuffer({ "position": 0, "uvs": 1, "normals":3  })
    InterleavedElementBuffer.push("type0"), InterleavedElementBuffer.push("type1"), InterleavedElementBuffer.push("type2")
    or
    InterleavedElementBuffer.push_all(["packed_data"])
    
# SDF Atlases

  # SDF Grid Finish
    SDF Grid is a degenerate filled disgusting pool of trash of a an SDF atlas generator but to finish SDF Grid
    I need to be to find which pixels are inside of the curve.

    Step 1:
      Refactor all code related to sdf grid atlas generation.

# Program or "Material"
  ## Program ShaderProgram.py
  program:
  realistic usage
  ## Future plans
    not all uniforms need to be updated when only a single must be updated
    having a reference to a value is useful so that copies are not neccecary, so there should be a way
    to set the names of all uniforms which need updating then just update those I guess
  realistic usage
    shader_program = ShaderProgram({
      "vertex_shader" : (string or file)
      "fragment_shader" : (string or file),
      uniforms: {
        "name": {type:"sampler2D", value: text2D}
      }
    })


    shader_program.uniforms = {
      "name of uniform" : {type, value}   
    }

    shader_program.set_uniform("world_span", value)

# Uniform buffer
  realistic usage
    uniform_buffer = UniformBuffer(data)
    shader_program.uniforms.ultimate_zone = uniform_buffer.block
    
# Text Machine

  pushing_text_advanced


  realistic usage
    text = Text("hello", [0.0, 0.0, 1.0, 1.0])
    text_machine.add(text)
    
    the usage of the data texture and its disposability hinges on usage as if each vector push is purely a pixel, such that it can be updated properly

    word groups  a change in one results in a change in all the text is assigned the gorup ID [int,int,int,int,int]
    and I suppose a reference to their DataTexture or atleast the texture machine itself.

    the dilema, instead of storing the beginning of a block, it might be neccecary to store all tails to each individual vector pushed
    such that certain pixels could be reused.

    so when its like text.set_position(x,y,z) then internally the text calls the text_machine, then says update group id.

    the entire text object should have its particular uniform id/index into the text machine, given to the text object so it can be changed or altered.
    then in the particular ui system, a map can be sent for the text objects.
    # text machine adds its self as a reference to the text
  
    # basic usage
    # t = text_machine(scene, "joan")
    
    # to = text()
    # to.text = "hi"

    # t.add(to)

# Texture
  realisitc usage
  Static Data:    
    data = []
    t = Texture(state, width, height, data, {
      "dimension": "2D",
      "format": GL_RGB,
      "type": GL_FLOAT,
    })

    
  Dynamic Data:

    t = Texture(state, width, height, data, {
      "dimension": "2D",
      "format": GL_RGB,
      "type": GL_FLOAT,
    })

    add_object(x,y,z,w)
      Push by pixel so for example sub routine
      t.push( x )
      t.push( y )
      t.push( z )
      t.push( w )

    requires that internal data storeage is created

      
    
    

  





# Frustrum UI

  expand glml nodes to account for math nodes
  or create a parser which will parse math functions
  and return content info based on the limiting container as before

  frustrum UI takes the document tree and simply renders it with respect
  the current state of the frustrum at the time it is "rendered"p




  changes between transform glml and frustrum ui
  the calculated container, a better idea would be to actually just
  keep everything the same but project the glml node with the same view matrix and projection matrix.

  future note that this module is nearly obsolete


    

# DEV LOG 3
finish event animation system, ready to add new attributes and object types
add frustrum ui system with LaTex parser

