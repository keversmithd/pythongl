
import copy

class union_event_point:
    segment = 0
    point = 0
    def __init__(self,segment,point):
        self.segment = segment
        self.point = point


def union_event_point_compare(uep0):
    return uep0.point

def overlap_share_endpoint(segment0,segment1):

    if(segment0[0] == segment1[0] and segment0[1] == segment1[1]):
        return False
    
    if(segment0[0] == segment1[0] or segment0[1] == segment1[1]):
        return True

    if(segment0[0] > segment1[0] and segment0[0] < segment1[1]) or (segment0[0] < segment1[0] and segment0[1] > segment1[0]):
        return True
    
    return False



def unionize_segments(segments):

    union_event_points = []

    for segment in segments:
        union_event_points.append(union_event_point(segment,segment[0]))
        union_event_points.append(union_event_point(segment,segments[1]))

    sorted_union_event_points = sorted(union_event_points,union_event_point_compare)

    combined_segments = []
    combined_tail = 0

    for i in range(0,len(sorted_union_event_points)):
        event_segment = sorted_union_event_points[i].segment
        if(len(combined_segments) == 0):
            combined_segments.append(copy.deepcopy(event_segment))
        else:
            segment_tail = combined_segments[combined_tail]
            if(overlap_share_endpoint(event_segment,segment_tail)):
                combined_segments[combined_tail][0] = min(event_segment[0],segment_tail[0])
                combined_segments[combined_tail][1] = max(event_segment[1],segment_tail[1])
            else:
                combined_tail += 1
                combined_segments.append(copy.deepcopy(event_segment))


