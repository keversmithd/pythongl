#version 460 core

layout(location = 0) vec3 position;
layout(location = 1) vec3 orientation;
layout(location = 2) vec3 color;
layout(location = 3) vec3 char_stats;

out VertexData
{
    vec3 position;
    vec3 orientation;
    vec3 color;
    vec3 char_stats;
} outData;

void main()
{

    outData.position = position;
    outData.orientation = orientation;
    outData.color = color;
    outData.char_stats = char_stats;

    gl_Position = vec4(0.0,0.0,0.0,0.0);

}