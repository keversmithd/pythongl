
def bounding_from_triangle(triangle):

    minX = triangle[0][0]
    minY = triangle[0][1]
    minZ = triangle[0][2]

    minX = min(minX, triangle[1][0])
    minX = min(minX, triangle[2][0])

    minY = min(minY, triangle[1][1])
    minY = min(minY, triangle[2][1])

    minZ = min(minZ, triangle[2][2])
    minZ = min(minZ, triangle[2][2])


    maxX = triangle[0][0]
    maxY = triangle[0][1]
    maxZ = triangle[0][2]


    maxX = max(maxX, triangle[1][0])
    maxX = max(maxX, triangle[2][0])

    maxY = max(maxY, triangle[1][1])
    maxY = max(maxY, triangle[2][1])

    maxZ = max(maxZ, triangle[2][2])
    maxZ = max(maxZ, triangle[2][2])

    return [[minX,minY,minZ],[maxX,maxY,maxZ]]

def split_bounding(bounding_domain):

    lX = bounding_domain[0][0]
    lY = bounding_domain[0][1]
    lZ = bounding_domain[0][2]

    rX = bounding_domain[1][0]
    rY = bounding_domain[1][1]
    rZ = bounding_domain[1][2]

    Xrange = rX-lX
    Yrange = rY-lY
    Zrange = rZ-lZ
    
    midX = lX + (Xrange/2)
    midY = lY + (Yrange/2)
    midZ = lZ + (Zrange/2)

    b0 = [[lX,lY,lZ],[midX,midY,midZ]]
    b1 = [[midX,lY,lZ],[rX,midY,midZ]]
    b2 = [[midX,midY,lZ],[rX,rY,midZ]]
    b3 = [[lX,midY,lZ],[midX,rY,midZ]]

    b4 = [[lX,lY,lZ],[midX,midY,rZ]]
    b5 = [[midX,lY,lZ],[rX,midY,rZ]]
    b6 = [[midX,midY,lZ],[rX,rY,rZ]]
    b7 = [[lX,midY,lZ],[midX,rY,rZ]]

    return [b0,b1,b2,b3,b4,b5,b6,b7]
    
def bounding_intersection(bounding_domain, object_domain):

    left = object_domain[0][0]
    right = object_domain[1][0]

    bottom = object_domain[0][1]
    top = object_domain[1][1]

    front = object_domain[0][2]
    back = object_domain[1][2]

    x_left = bounding_domain[0][0]
    x_right = bounding_domain[1][0]

    x_bottom = bounding_domain[0][1]
    x_top = bounding_domain[1][1]

    x_front = bounding_domain[0][2]
    x_back = bounding_domain[1][2]


    #case 1
    b0 = left > x_left and left <= x_right
    b1 = bottom > x_bottom and bottom <= x_top
    b2 = front < x_front and front > x_back

    #case 2
    c0 = left < x_left and right > x_left
    c1 = bottom < bottom and top > x_bottom
    c2 = front < x_front and front > x_back

    return (b0 and b1 and b2) or (c0 and c1 and c2)


    #case 1
    #left > x_left and left <= x_right and
    #bottom > x_bottom and bottom <= x_top and
    #front < x_front and front > x_back and

    #case 2
    #left < x_left and right > x_left and
    #bottom < bottom and top > bottom and
    #front > front and back < back



def bounding_intersection_list(split_bounding, object_domain):
    intersections = []
    for i in range(0,len(split_bounding)):
        if(bounding_intersection(split_bounding[i], object_domain)):
            intersections.append(i)
    return intersections
