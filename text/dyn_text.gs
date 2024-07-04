#version 460 core
layout(points) in;
layout(triangle_strip, max_vertices=3) out;

in VertexData
{
  vec3 position;
  vec3 orientation;
  vec3 color;
  vec3 char_stats;

} inData[];

out VertexData
{
    vec3 color;
    vec3 orientation;
} outData;

uniform char_count;

layout(std430, binding = 3) ConstTextBuffer
{
    int start_stop = [];
    int index_map[];
    vec3 geometry[];
    vec3 indices[];
};

const pi = 3.14159265359;


vec3 rotateVec(vec3 vec, float angle)
{
    c = cos(angle);
    s = sin(angle);
    #in sequence
    #x = x
    #y = c*y - s*z
    #z = s*y  + c*z

    #x = c*x +s*y
    #y = y
    #z = -s*x + c*z

    #x = c*x -s*y
    #y = s*x + c*y
    #z = z
    #all at once
    #x = x + c*x + s*z + c*x -s*y
    #y = y*c - s*z + y +s*x +  c*y
    #z = y*s - c*z -s*x +  c*z + z

    float x = vec.x * (c + c) + vec.y * (-s) + vec.z * (s - s);
    float y = vec.x * (s + s) + vec.y * c + vec.z * (-s + s);
    float z = vec.x * (-s) + vec.y * (s - s) + vec.z * (c + c);

    return vec3(x,y,z);
}


vec4 hamil(vec4 q1, vec4 q2)
{
    return vec4(q1.x*q2.x - q1.y*q2.y - q1.z*q2.z - q1.w*q2.w,
                q1.x*q2.y + q1.y*q2.x + q1.z*q2.w - q1.w*q2.z,
                q1.x*q2.z - q1.y*q2.w + q1.z*q2.x + q1.w*q2.y,
                q1.x*q2.w + q1.y*q2.z - q1.z*q2.y + q1.w*q2.x);
}

vec3 rotateAboutVec(vec3 v, vec3 n, float angle)
{
    c = cos(angle);
    s = sin(angle);
    n  = normalize(n);
    rotQuat = vec4(cos(angle/2),n.x*sin(angle/2),n.y*sin(angle/2),n.z*sin(angle/2));
    conj = vec4(rotQuat.x,-rotQuat.y,-rotQuat.z,-rotQuat.w);
    vec4 p = vec4(0, v.x, v.y,v.z);
    vec4 R = hamil(hamil(rotQuat,p),conj);
    return R.yzw;

}

vec3 rotateToNormal(vec3 vertex, vec3 normal)
{
    vec3 norm = vec3(0,0,1);
    vec3 aperp = normalize(cross(norm,normal));
    d = dot(norm,normal);

    identical = (vertex.x==normal.x) && (vertex.y==normal.y) && (vertex.z == normal.z);
    if(identical)
    {
        return vertex;
    }
    a = 0.0;
    ma = length(norm);
    mb = length(normal);
    if(d == 0)
    {
        a = pi;

    }else
    {
        a = acos(d/(ma*mb));
    }

    return rotateAboutVec(vertex, aperp, a);

}

void main()
{
    
    int char_id =  int(inData[0].char_stats.x);
    int char_index = index_map[char_id]
    int start  =  start_stop[char_index]
    int end    =  start_stop[char_index+1]

    int vertexes_computed = 0;
    

    for (int i = start; i < end; i++)
    {
        int vertex_index = index_map[i];
        vec3 vertex = geometry[vertex_index];
        //proccessing here | processing good because normal always same

        vertex.x+=(position.x*char_stats.y);
        vertex.y+=(position.y*char_stats.z);
        vertex.z+=position.z;
        vertex = rotateToNormal(vertex, inData[0].orientation);

        outData.color = inData[0].color;
        outData.orientation = inData[0].orientation;

        gl_Position = vec4(vertex,1.0);
        EmitVertex();

        vertexes_computed += 1;
        if(vertexes_computed % 3 == 0)
        {
            EndPrimitive();
        }


    }






}