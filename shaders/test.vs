#version 460 core

layout(location = 1) in vec3 pos;


void main()
{

    gl_Position = vec4(pos,1);
}