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
 ## optimizations
  every element traversal is neccecary
  need to store id's which link to node for faster selection
  the element itself should have optimal uniform structure
  

## DEV LOG 2 

1st hour build element which is versatile and usable to instantiate with the ui transformer, this also involves a way to wrap and deliver the objects the scene. 

since MVP of the inital element has a flaw of many buffer updates for its uniform there are refactors which can help, such as instancing, maybe using like a shader control to write the updates to a uniform texture which has like one draw call but still updates [save for later]


2nd build event object which abstracts the partitioning data structure but delivers real time collsiion results ot objects.