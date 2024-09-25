import math

class Euler:

    def __init__( self, x=0,y=0,z=0 ):

        self.vec = [x,y,z]

        return
    
    def setFromAxisAngle0(self, axis, angle):
        # Convert angle from degrees to radians
        angle_rad = angle * math.pi / 180

        s = math.sin(angle_rad / 2)
        c = math.cos(angle_rad / 2)

        ax = axis[0]
        ay = axis[1]
        az = axis[2]

        # Normalize the axis vector
        magnitude = math.sqrt(ax * ax + ay * ay + az * az)
        if magnitude == 0:
            return self.vec

        ax /= magnitude
        ay /= magnitude
        az /= magnitude

        x = ax * s
        y = ay * s
        z = az * s
        w = c

        # Convert quaternion (x, y, z, w) to Euler angles (roll, pitch, yaw)
        # Assuming the order of rotation is Yaw (Z), Pitch (Y), and Roll (X)
        ysqr = y * y

        # Roll (X-axis rotation)
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + ysqr)
        roll = math.atan2(t0, t1)

        # Pitch (Y-axis rotation)
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch = math.asin(t2)

        # Yaw (Z-axis rotation)
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (ysqr + z * z)
        yaw = math.atan2(t3, t4)

        # Convert radians back to degrees
        self.vec[0] = roll * 180 / math.pi
        self.vec[1] = pitch * 180 / math.pi
        self.vec[2] = yaw * 180 / math.pi

        return self.vec

    def setFromAxisAngle(self, axis, angle):

        a = angle*math.pi/180

        s = math.sin( a )
        c = math.cos( a )
        t = (1-c)

        ax = axis[0]
        ay = axis[1]
        az = axis[2]

        magnitude = math.sqrt ( ax*ax + ay*ay + az*az )

        if ( magnitude == 0 ):
            return self.vec
        
        ax = ax/magnitude
        ay = ay/magnitude
        az = az/magnitude

        if ((ax*ay*t + az*s) > 0.998 ):

            self.vec[1] = 2*math.atan2(ax*math.sin(a/2), math.cos(a/2))
            self.vec[2] = math.pi/2
            self.vec[0] = 0
            return self.vec
        
        if ((ax*ay*t + az*s) < -0.998 ):

            self.vec[1] = -2*math.atan2(ax*math.sin(a/2), math.cos(a/2))
            self.vec[2] = -math.pi/2
            self.vec[0] = 0
            return self.vec


        self.vec[1] = math.atan2 ( ay*s - ax*az*t, 1-((ay*ay) + (az*az))*t  )*180/math.pi
        self.vec[2] = math.asin( ax*ay*t + az*s )*180/math.pi
        self.vec[0] = math.atan2 ( ax*s-ay*az*t, 1-(ax*ax + az*az)*t )*180/math.pi

        return self.vec

        
    