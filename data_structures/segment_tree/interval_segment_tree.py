
class interval_segment_node:
    value = 0
    segment = (0,0)
    def __init__(self,value,segment):
        self.segment[0] = segment[0]
        self.segment[1] = segment[1]
        self.value = value


class interval_segment_tree:

    tree = []

    def __init__(self, N):
        self.tree = [0] * (2*N)
        return
    
    def construct(self,I):
        
        interval_points = []

        for i in range(len(I)):
            interval_points.append(I[i][0])
            interval_points.append(I[i][1])
        
        interval_points.sort()

        for i in range(len(interval_points)):
            self.insert_value_with_interval(interval_points[i],I[int(i/2)])


    #def insert_value_with_interval(value,interval):


