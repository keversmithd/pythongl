# glml transformer from pc
 transform glml state into elements
 the transformer takes the attribute data and parses it using the current graphics state
 the graphics state contains information about window size, pixel length etc
 in order to update the desired units in real time the transformer must act graphics context callbacks
 the transformer will say transform, it will make a parallel tree using the ui units which are graphics objects
 this tree will then be updated by traversing and updating the uniforms of the appropriate ui objects
## glml transformer algorithm
 traverse tree, find conversions to ui objects by name
 update the attributes based on current state [running state object]
 and compile the objects into the tree
## basic interaction
 need data structure for spatial partitioning, will be a normalized grid, were the event objects eject and reinster them selves, the span between the two extremas will insert into the grid, when the object is changed it will reinsert itself
 then there must be an option for sub granular detection, and z-depth

# Layout elemement machine instanced

  layout_element_machine()
  .add_element({ container, parent_container, relation, color })

  ## to do
    border, stroke, opacity, etc.
    
# Text machine

  ideal usage
    text_id = text_machine.Text("text_machine1")

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
    return index groups for mutable section or vertices of the buffer, and a region expansions algorithm to measure the regions which
    need update.
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

      
    
    

  





## DEV LOG 2 
1st hour build element which is versatile and usable to instantiate with the ui transformer, this also involves a way to wrap and deliver the objects the scene. 

since MVP of the inital element has a flaw of many buffer updates for its uniform there are refactors which can help, such as instancing, maybe using like a shader control to write the updates to a uniform texture which has like one draw call but still updates [save for later]


2nd build event object which abstracts the partitioning data structure but delivers real time collsiion results ot objects.